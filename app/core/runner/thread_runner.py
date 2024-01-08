import logging

from typing import List
from concurrent.futures import Executor

from config.llm import llm_settings, tool_settings

from app.api.deps import get_session
import app.core.runner.utils.message_util as msg
from app.core.runner.utils.tool_call_util import (
    tool_call_recognize,
    internal_tool_call_invoke,
    tool_call_request,
    tool_call_id,
    tool_call_output,
)
from app.core.runner.llm_backend import LLMBackend
from app.core.runner.context_integration_policy import context_integration_policy
from app.core.tools import tool_find, BaseTool
from app.libs.thread_executor import get_executor_for_config, run_with_executor
from app.models.run_step import RunStep
from app.models.run import Run
from app.models.message import Message
from app.services.message.message import MessageService
from app.services.run.run import RunService
from app.services.run.run_step import RunStepService


class ThreadRunner:
    """
    ThreadRunner 封装 run 的执行逻辑
    """
    tool_executor: Executor = get_executor_for_config(tool_settings.TOOL_WORKER_NUM, "tool_worker_")

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.session = next(get_session())
        self.llm = LLMBackend(llm_settings=llm_settings)
        self.max_step = llm_settings.LLM_MAX_STEP

    def run(self):
        """
        完成一次 run 的执行，基本步骤
        1. 初始化，获取 run 以及相关 tools， 构造 system instructions;
        2. 开始循环，查询已有 run step，进行 chat message 生成;
        3. 调用 llm 并解析返回结果;
        4. 根据返回结果，生成新的 run step(tool calls 处理) 或者 message
        """
        run = RunService.get_run(session=self.session, run_id=self.run_id)
        run = RunService.to_in_progress(session=self.session, run_id=self.run_id)
        logging.info("processing ThreadRunner task, run_id: %s", self.run_id)

        tools = [tool_find(tool, lambda tool: tool["type"]) for tool in run.tools]

        instructions = [run.instructions]
        for tool in tools:
            tool.configure(session=self.session, run=run)
            instruction_supplement = tool.instruction_supplement()
            if instruction_supplement:
                instructions += [instruction_supplement]
        instruction = "\n".join(instructions)

        loop = True
        while loop:
            run_steps = RunStepService.get_run_step_list(
                session=self.session, run_id=self.run_id, thread_id=run.thread_id
            )
            loop = self.__run_step(run, run_steps, instruction, tools)

    def __run_step(self, run: Run, run_steps: List[RunStep], instruction: str, tools: List[BaseTool]):
        """
        执行 run step
        """
        logging.info("step %d is running", len(run_steps) + 1)

        assistant_system_message = [msg.system_message(instruction)]

        # 获取已有 message 上下文记录
        chat_messages = self.__generate_chat_messages(
            MessageService.get_message_list(session=self.session, thread_id=run.thread_id)
        )

        tool_call_messages = []
        for step in run_steps:
            if step.type == "tool_calls" and step.status == "completed":
                tool_call_messages += self.__convert_assistant_tool_calls_to_chat_messages(step)

        messages = context_integration_policy.integrate_context(
            assistant_system_message + chat_messages + tool_call_messages
        )
        response_msg = self.llm.run(
            messages=messages,
            model=run.model,
            tools=[tool.openai_function for tool in tools],
            tool_choice="auto" if len(run_steps) < self.max_step else "none",
        )

        if msg.is_tool_call(response_msg):
            # tool & tool_call definition dict
            tool_calls = [tool_call_recognize(tool_call, tools) for tool_call in response_msg.tool_calls]

            # new run step for tool calls
            new_run_step = RunStepService.new_run_step(
                session=self.session,
                type="tool_calls",
                assistant_id=run.assistant_id,
                thread_id=run.thread_id,
                run_id=run.id,
                step_details={"type": "tool_calls", "tool_calls": [tool_call_dict for _, tool_call_dict in tool_calls]},
            )

            internal_tool_calls = list(filter(lambda tool_calls: tool_calls[0] is not None, tool_calls))
            external_tool_call_dict = [tool_call_dict for tool, tool_call_dict in tool_calls if tool is None]

            # 为减少线程同步逻辑，依次处理内/外 tool_call 调用
            if internal_tool_calls:
                try:
                    tool_calls_with_outputs = run_with_executor(
                        executor=ThreadRunner.tool_executor,
                        func=internal_tool_call_invoke,
                        tasks=internal_tool_calls,
                        timeout=tool_settings.TOOL_WORKER_EXECUTION_TIMEOUT,
                    )
                    RunStepService.update_step_details(
                        session=self.session,
                        run_step_id=new_run_step.id,
                        step_details={"type": "tool_calls", "tool_calls": tool_calls_with_outputs},
                        completed=not external_tool_call_dict,
                    )
                except Exception as e:
                    RunStepService.to_failed(session=self.session, run_step_id=new_run_step.id, last_error=e)
                    raise e

            if external_tool_call_dict:
                # run 设置为 action required，等待业务完成更新并再次拉起
                RunService.to_requires_action(
                    session=self.session,
                    run_id=run.id,
                    required_action={
                        "type": "submit_tool_outputs",
                        "submit_tool_outputs": {"tool_calls": external_tool_call_dict},
                    },
                )
            else:
                return True
        else:
            # 无 tool call 信息，创建 message，结束任务
            new_message = MessageService.new_message(
                session=self.session,
                role=response_msg.role,
                content=response_msg.content,
                assistant_id=run.assistant_id,
                thread_id=run.thread_id,
                run_id=run.id,
            )

            RunStepService.new_run_step(
                session=self.session,
                type="message_creation",
                assistant_id=run.assistant_id,
                thread_id=run.thread_id,
                status="completed",
                run_id=run.id,
                step_details={"type": "message_creation", "message_creation": {"message_id": new_message.id}},
            )
            RunService.to_completed(session=self.session, run_id=run.id)

        # 任务结束
        return False

    def __generate_chat_messages(self, messages: List[Message]):
        """
        根据历史信息生成 chat message
        """

        # message 构造
        def message_mapping(message: Message):
            role = message.role

            if role == "system" or role == "assistant" or role == "user":
                message_content = message.content[0]["text"]["value"]
                return msg.new_message(role, message_content)
            else:
                pass

        return [message_mapping(msg) for msg in messages]

    def __convert_assistant_tool_calls_to_chat_messages(self, run_step: RunStep):
        """
        根据 run step 执行结果生成 message 信息
        每个 tool call run step 包含两部分，调用与结果(结果可能为多个信息)
        """
        tool_calls = run_step.step_details["tool_calls"]
        tool_call_requests = [msg.tool_calls([tool_call_request(tool_call) for tool_call in tool_calls])]
        tool_call_outputs = [
            msg.tool_call_result(tool_call_id(tool_call), tool_call_output(tool_call)) for tool_call in tool_calls
        ]
        return tool_call_requests + tool_call_outputs
