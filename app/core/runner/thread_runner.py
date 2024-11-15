from functools import partial
import logging

from typing import List
from concurrent.futures import Executor

from sqlalchemy.orm import Session

from app.models.token_relation import RelationType
from config.config import settings
from config.llm import llm_settings, tool_settings

from app.core.runner.llm_backend import LLMBackend
from app.core.runner.llm_callback_handler import LLMCallbackHandler
from app.core.runner.memory import Memory, find_memory
from app.core.runner.pub_handler import StreamEventHandler
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
from app.models.message import Message, MessageUpdate
from app.models.run import Run
from app.models.run_step import RunStep
from app.models.token_relation import RelationType
from app.services.assistant.assistant import AssistantService
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

    def __init__(self, run_id: str, session: Session, stream: bool = False):
        self.run_id = run_id
        self.session = session
        self.stream = stream
        self.max_step = llm_settings.LLM_MAX_STEP
        self.event_handler: StreamEventHandler = None

    def run(self):
        """
        完成一次 run 的执行，基本步骤
        1. 初始化，获取 run 以及相关 tools, 构造 system instructions;
        2. 开始循环，查询已有 run step, 进行 chat message 生成;
        3. 调用 llm 并解析返回结果;
        4. 根据返回结果，生成新的 run step(tool calls 处理) 或者 message
        """
        # TODO: 重构，将 run 的状态变更逻辑放到 RunService 中
        run = RunService.get_run_sync(session=self.session, run_id=self.run_id)
        self.event_handler = StreamEventHandler(run_id=self.run_id, is_stream=self.stream)

        run = RunService.to_in_progress(session=self.session, run_id=self.run_id)
        self.event_handler.pub_run_in_progress(run)
        logging.info("processing ThreadRunner task, run_id: %s", self.run_id)

        # get memory from assistant metadata
        # format likes {"memory": {"type": "window", "window_size": 20, "max_token_size": 4000}}
        ast = AssistantService.get_assistant_sync(session=self.session, assistant_id=run.assistant_id)
        metadata = ast.metadata_ or {}
        memory = find_memory(metadata.get("memory", {}))

        instructions = [run.instructions] if run.instructions else [ast.instructions]
        tools = find_tools(run, self.session)
        for tool in tools:
            tool.configure(session=self.session, run=run)
            instruction_supplement = tool.instruction_supplement()
            if instruction_supplement:
                instructions += [instruction_supplement]
        instruction = "\n".join(instructions)

        llm = self.__init_llm_backend(run.assistant_id)
        loop = True
        while loop:
            run_steps = RunStepService.get_run_step_list(
                session=self.session, run_id=self.run_id, thread_id=run.thread_id
            )
            loop = self.__run_step(llm, run, run_steps, instruction, tools, memory)

        # 任务结束
        self.event_handler.pub_run_completed(run)
        self.event_handler.pub_done()

    def __run_step(
        self,
        llm: LLMBackend,
        run: Run,
        run_steps: List[RunStep],
        instruction: str,
        tools: List[BaseTool],
        memory: Memory,
    ):
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

        # memory
        messages = assistant_system_message + memory.integrate_context(chat_messages) + tool_call_messages 

        response_stream = llm.run(
            messages=messages,
            model=run.model,
            tools=[tool.openai_function for tool in tools],
            tool_choice="auto" if len(run_steps) < self.max_step else "none",
            stream=True,
            stream_options=run.stream_options,
            extra_body=run.extra_body,
            temperature=run.temperature,
            top_p=run.top_p,
            response_format=run.response_format,
        )

        # create message callback
        create_message_callback = partial(
            MessageService.new_message,
            session=self.session,
            assistant_id=run.assistant_id,
            thread_id=run.thread_id,
            run_id=run.id,
            role="assistant",
        )

        # create 'message creation' run step callback
        def _create_message_creation_run_step(message_id):
            return RunStepService.new_run_step(
                session=self.session,
                type="message_creation",
                assistant_id=run.assistant_id,
                thread_id=run.thread_id,
                run_id=run.id,
                step_details={"type": "message_creation", "message_creation": {"message_id": message_id}},
            )

        llm_callback_handler = LLMCallbackHandler(
            run_id=run.id,
            on_step_create_func=_create_message_creation_run_step,
            on_message_create_func=create_message_callback,
            event_handler=self.event_handler,
        )
        response_msg = llm_callback_handler.handle_llm_response(response_stream)
        message_creation_run_step = llm_callback_handler.step
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
            self.event_handler.pub_run_step_created(new_run_step)
            self.event_handler.pub_run_step_in_progress(new_run_step)

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
                    new_run_step = RunStepService.update_step_details(
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
                run = RunService.to_requires_action(
                    session=self.session,
                    run_id=run.id,
                    required_action={
                        "type": "submit_tool_outputs",
                        "submit_tool_outputs": {"tool_calls": external_tool_call_dict},
                    },
                )
                self.event_handler.pub_run_step_delta(
                    step_id=new_run_step.id, step_details={"type": "tool_calls", "tool_calls": external_tool_call_dict}
                )
                self.event_handler.pub_run_requires_action(run)
            else:
                self.event_handler.pub_run_step_completed(new_run_step)
                return True
        else:
            # 无 tool call 信息，message 生成结束，更新状态
            new_message = MessageService.modify_message_sync(
                session=self.session,
                thread_id=run.thread_id,
                message_id=llm_callback_handler.message.id,
                body=MessageUpdate(content=response_msg.content),
            )
            self.event_handler.pub_message_completed(new_message)

            new_step = RunStepService.update_step_details(
                session=self.session,
                run_step_id=message_creation_run_step.id,
                step_details={"type": "message_creation", "message_creation": {"message_id": new_message.id}},
                completed=True,
            )
            RunService.to_completed(session=self.session, run_id=run.id)
            self.event_handler.pub_run_step_completed(new_step)

        return False

    def __init_llm_backend(self, assistant_id):
        if settings.AUTH_ENABLE:
            # init llm backend with token id
            token_id = TokenRelationService.get_token_id_by_relation(
                session=self.session, relation_type=RelationType.Assistant, relation_id=assistant_id
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

        chat_messages = []
        for message in messages:
            role = message.role
            if role == "user":
                message_content = []
                if message.file_ids:
                    files = FileService.get_file_list_by_ids(session=self.session, file_ids=message.file_ids)
                    for file in files:
                        chat_messages.append(msg_util.new_message(role, f'The file "{file.filename}" can be used as a reference'))
                else:
                    for content in message.content:
                        if content["type"] == "text":
                            message_content.append({"type": "text", "text": content["text"]["value"]})
                        elif content["type"] == "image_url":
                            message_content.append(content)
                    chat_messages.append(msg_util.new_message(role, message_content))
            elif role == "assistant":
                message_content = ""
                for content in message.content:
                    if content["type"] == "text":
                        message_content += content["text"]["value"]
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
