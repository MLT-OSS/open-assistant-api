from datetime import datetime
from typing import List, Tuple, Optional
from fastapi import Request
from sse_starlette import EventSourceResponse
from openai.types.beta import assistant_stream_event as events

from app.exceptions.exception import ResourceNotFoundError, InternalServerError
from app.providers.database import redis_client

"""
LLM chat message event pub/sub handler
"""


def generate_channel_name(key: str) -> str:
    return f"generate_event:{key}"


def channel_exist(channel: str) -> bool:
    return bool(redis_client.keys(channel))


def pub_event(channel: str, data: dict) -> None:
    """
    publish events to channel
    :param channel: channel name
    :param event: event dict
    """
    redis_client.xadd(channel, data)
    redis_client.expire(channel, 10 * 60)


def read_event(channel: str, x_index: str = None) -> Tuple[Optional[str], Optional[dict]]:
    """
    Read events from the channel, starting from the next index of x_index
    :param channel: channel name
    :param x_index: previous event_id, first time is empty
    :return: event index, event data
    """
    if not x_index:
        x_index = "0-0"

    data = redis_client.xread({channel: x_index}, count=1, block=180_000)
    if not data:
        return None, None

    stream_id = data[0][1][0][0]
    event = data[0][1][0][1]
    return stream_id, event


def save_last_stream_id(run_id: str, stream_id: str):
    """
    保存当前 run_id 对应的最新 stream_id
    :param run_id: 当前的运行 ID
    :param stream_id: 最新的 stream_id
    """
    redis_client.set(f"run:{run_id}:last_stream_id", stream_id, 10 * 60)


def get_last_stream_id(run_id: str) -> str:
    """
    获取上次保存的 stream_id
    :param run_id: 当前的运行 ID
    :return: 上次的 stream_id 或 None
    """
    return redis_client.get(f"run:{run_id}:last_stream_id")


def _data_adjust_tools(tools: List[dict]) -> List[dict]:
    def _adjust_tool(tool: dict):
        if tool["type"] not in {"code_interpreter", "file_search", "function"}:
            return {
                "type": "function",
                "function": {
                    "name": tool["type"],
                },
            }
        else:
            return tool

    if tools:
        return [_adjust_tool(tool) for tool in tools]
    return []


def _data_adjust(obj):
    """
    event data adjust:
    """
    id = obj.id
    data = obj.model_dump(exclude={"id"})
    data.update({"id": id})
    if hasattr(obj, "tools"):
        data["tools"] = _data_adjust_tools(data["tools"])

    if hasattr(obj, "file_ids") and data["file_ids"] is None:
        data["file_ids"] = []

    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.timestamp()
    return data


def _data_adjust_message(obj):
    data = _data_adjust(obj)
    if "status" not in data:
        data["status"] = "in_progress"
    return data


def _data_adjust_message_delta(step_details):
    for index, tool_call in enumerate(step_details["tool_calls"]):
        tool_call["index"] = index
    return step_details


def sub_stream(run_id, request: Request, prefix_events: List[dict] = [], suffix_events: List[dict] = []):
    """
    Subscription chat response stream
    """
    channel = generate_channel_name(run_id)

    async def _stream():
        for event in prefix_events:
            yield event

        last_index = get_last_stream_id(run_id)  # 获取上次的 stream_id
        x_index = last_index or None
        while True:
            if await request.is_disconnected():
                break
            if not channel_exist(channel):
                raise ResourceNotFoundError()

            x_index, data = read_event(channel, x_index)
            if not data:
                break

            if data["event"] == "done":
                save_last_stream_id(run_id, x_index)  # 记录最新的 stream_id
                break

            if data["event"] == "error":
                save_last_stream_id(run_id, x_index)  # 记录最新的 stream_id
                raise InternalServerError(data["data"])

            yield data
            save_last_stream_id(run_id, x_index)  # 记录最新的 stream_id

        for event in suffix_events:
            yield event

    return EventSourceResponse(_stream())


class StreamEventHandler:
    def __init__(self, run_id: str, is_stream: bool = False) -> None:
        self._channel = generate_channel_name(key=run_id)
        self._is_stream = is_stream

    def pub_event(self, event) -> None:
        if self._is_stream:
            pub_event(self._channel, {"event": event.event, "data": event.data.json()})

    def pub_run_created(self, run):
        self.pub_event(events.ThreadRunCreated(data=_data_adjust(run), event="thread.run.created"))

    def pub_run_queued(self, run):
        self.pub_event(events.ThreadRunQueued(data=_data_adjust(run), event="thread.run.queued"))

    def pub_run_in_progress(self, run):
        self.pub_event(events.ThreadRunInProgress(data=_data_adjust(run), event="thread.run.in_progress"))

    def pub_run_completed(self, run):
        self.pub_event(events.ThreadRunCompleted(data=_data_adjust(run), event="thread.run.completed"))

    def pub_run_requires_action(self, run):
        self.pub_event(events.ThreadRunRequiresAction(data=_data_adjust(run), event="thread.run.requires_action"))

    def pub_run_failed(self, run):
        self.pub_event(events.ThreadRunFailed(data=_data_adjust(run), event="thread.run.failed"))

    def pub_run_step_created(self, step):
        self.pub_event(events.ThreadRunStepCreated(data=_data_adjust(step), event="thread.run.step.created"))

    def pub_run_step_in_progress(self, step):
        self.pub_event(events.ThreadRunStepInProgress(data=_data_adjust(step), event="thread.run.step.in_progress"))

    def pub_run_step_delta(self, step_id, step_details):
        self.pub_event(
            events.ThreadRunStepDelta(
                data={
                    "id": step_id,
                    "delta": {"step_details": _data_adjust_message_delta(step_details)},
                    "object": "thread.run.step.delta",
                },
                event="thread.run.step.delta",
            )
        )

    def pub_run_step_completed(self, step):
        self.pub_event(events.ThreadRunStepCompleted(data=_data_adjust(step), event="thread.run.step.completed"))

    def pub_run_step_failed(self, step):
        self.pub_event(events.ThreadRunStepFailed(data=_data_adjust(step), event="thread.run.step.failed"))

    def pub_message_created(self, message):
        self.pub_event(events.ThreadMessageCreated(data=_data_adjust_message(message), event="thread.message.created"))

    def pub_message_in_progress(self, message):
        self.pub_event(
            events.ThreadMessageInProgress(data=_data_adjust_message(message), event="thread.message.in_progress")
        )

    def pub_message_usage(self, chunk):
        """
        目前 stream 未有 usage 相关 event，借用 thread.message.in_progress 进行传输，待官方更新
        """
        data = {
            "id": chunk.id,
            "content": [],
            "created_at": 0,
            "object": "thread.message",
            "role": "assistant",
            "status": "in_progress",
            "thread_id": "",
            "metadata": {"usage": chunk.usage.json()}
        }
        self.pub_event(
            events.ThreadMessageInProgress(data=data, event="thread.message.in_progress")
        )

    def pub_message_completed(self, message):
        self.pub_event(
            events.ThreadMessageCompleted(data=_data_adjust_message(message), event="thread.message.completed")
        )

    def pub_message_delta(self, message_id, index, content, role):
        """
        pub MessageDelta
        """
        self.pub_event(
            events.ThreadMessageDelta(
                data=events.MessageDeltaEvent(
                    id=message_id,
                    delta={"content": [{"index": index, "type": "text", "text": {"value": content}}], "role": role},
                    object="thread.message.delta",
                ),
                event="thread.message.delta",
            )
        )

    def pub_done(self):
        pub_event(self._channel, {"event": "done", "data": "done"})

    def pub_error(self, msg):
        pub_event(self._channel, {"event": "error", "data": msg})
