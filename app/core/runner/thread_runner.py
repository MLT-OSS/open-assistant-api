import logging

from typing import List
from concurrent.futures import Executor

from config.llm import llm_settings, tool_settings
from config.config import settings


from app.api.deps import get_session
from app.core.doc_loaders import doc_loader
from app.core.runner.context_integration_policy import context_integration_policy
from app.core.runner.llm_backend import LLMBackend
from app.core.runner.llm_callback_handler import LLMCallbackHandler
from app.core.runner.utils import message_util as msg_util
from app.core.runner.utils.tool_call_util import (
    tool_call_recognize,
    internal_tool_call_invoke,
    tool_call_request,
    tool_call_id,
    tool_call_output,
)
from app.core.tools import find_tools, BaseTool
from app.libs.thread_executor import get_executor_for_config, run_with_executor
from app.models.message import Message
from app.models.run import Run
from app.models.run_step import RunStep
from app.models.file import File
from app.providers.storage import storage
from app.services.file.file import FileService
from app.services.message.message import MessageService
from app.services.run.run import RunService
from app.services.run.run_step import RunStepService
from app.services.token.token import TokenService
from app.services.token.token_relation import TokenRelationService


class ThreadRunner:
    """
    ThreadRunner 封装 run 的执行逻辑
    """

    tool_executor: Executor = get_executor_for_config(tool_settings.TOOL_WORKER_NUM, "tool_worker_")

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.session = next(get_session())
        self.max_step = llm_settings.LLM_MAX_STEP

    def run(self):
        """
        完成一次 run 的执行，基本步骤
        1. 初始化，获取 run 以及相关 tools， 构造 system instructions;
        2. 开始循环，查询已有 run step，进行 chat message 生成;
        3. 调用 llm 并解析返回结果;
        4. 根据返回结果，生成新的 run step(tool calls 处理) 或者 message
        """
        # TODO: 重构，将 run 的状态变更逻辑放到 RunService 中
        run = RunService.get_run(session=self.session, run_id=self.run_id)
        run = RunService.to_in_progress(session=self.session, run_id=self.run_id)
        logging.info("processing ThreadRunner task, run_id: %s", self.run_id)

        llm = self.__init_llm_backend(run.assistant_id)

        tools = find_tools(run, self.session)

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
            loop = self.__run_step(llm, run, run_steps, instruction, tools)

    def __run_step(self, llm: LLMBackend, run: Run, run_steps: List[RunStep], instruction: str, tools: List[BaseTool]):
        """
        执行 run step
        """
        logging.info("step %d is running", len(run_steps) + 1)

        assistant_system_message = [msg_util.system_message(instruction)]

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
        response_stream = llm.run(
            messages=messages,
            model=run.model,
            tools=[tool.openai_function for tool in tools],
            tool_choice="auto" if len(run_steps) < self.max_step else "none",
            stream=True,
            extra_body=run.extra_body,
        )

        # create message creation run step callback
        def _create_message_creation_run_step():
            return RunStepService.new_run_step(
                session=self.session,
                type="message_creation",
                assistant_id=run.assistant_id,
                thread_id=run.thread_id,
                run_id=run.id,
                step_details={"type": "message_creation"},
            )

        llm_callback_handler = LLMCallbackHandler(
            run_id=run.id, on_final_message_start_func=_create_message_creation_run_step
        )
        response_msg = llm_callback_handler.handle_llm_response(response_stream)
        message_creation_run_step = llm_callback_handler.on_final_message_start_func_output
        logging.info("chat_response_message: %s", response_msg)

        if msg_util.is_tool_call(response_msg):
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

            internal_tool_calls = list(filter(lambda _tool_calls: _tool_calls[0] is not None, tool_calls))
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

            RunStepService.update_step_details(
                session=self.session,
                run_step_id=message_creation_run_step.id,
                step_details={"type": "message_creation", "message_creation": {"message_id": new_message.id}},
                completed=True,
            )
            RunService.to_completed(session=self.session, run_id=run.id)

        # 任务结束
        return False

    def __init_llm_backend(self, assistant_id):
        if settings.AUTH_ENABLE:
            # init llm backend with token id
            token_id = TokenRelationService.get_token_id_by_relation(
                session=self.session, relation_type="assistant", relation_id=assistant_id
            )
            token = TokenService.get_token_by_id(self.session, token_id)
            return LLMBackend(base_url=token.llm_base_url, api_key=token.llm_api_key)
        else:
            # init llm backend with llm settings
            return LLMBackend(base_url=llm_settings.OPENAI_API_BASE, api_key=llm_settings.OPENAI_API_KEY)

    def __generate_chat_messages(self, messages: List[Message]):
        """
        根据历史信息生成 chat message
        """

        def file_load(file: File):
            file_data = storage.load(file.key)
            content = doc_loader.load(file_data)
            return f"For reference, here is is the content of file {file.filename}: '{content}'"

        chat_messages = []
        for message in messages:
            role = message.role

            if role == "system" or role == "assistant" or role == "user":
                message_content = []
                if role == "user" and message.file_ids:
                    files = FileService.get_file_list_by_ids(session=self.session, file_ids=message.file_ids)
                    for file in files:
                        chat_messages.append(msg_util.new_message(role, file_load(file)))
                else:
                    message_content = message.content[0]["text"]["value"]
                    chat_messages.append(msg_util.new_message(role, message_content))
        return chat_messages

    def __convert_assistant_tool_calls_to_chat_messages(self, run_step: RunStep):
        """
        根据 run step 执行结果生成 message 信息
        每个 tool call run step 包含两部分，调用与结果(结果可能为多个信息)
        """
        tool_calls = run_step.step_details["tool_calls"]
        tool_call_requests = [msg_util.tool_calls([tool_call_request(tool_call) for tool_call in tool_calls])]
        tool_call_outputs = [
            msg_util.tool_call_result(tool_call_id(tool_call), tool_call_output(tool_call)) for tool_call in tool_calls
        ]
        return tool_call_requests + tool_call_outputs
