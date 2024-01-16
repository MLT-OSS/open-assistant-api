from typing import Tuple, Optional

from app.providers.database import redis_client

"""
LLM chat message event pub/sub handler
"""


def generate_channel_name(key: str) -> str:
    return f"generate_result:{key}"


def channel_exist(channel: str) -> bool:
    return bool(redis_client.keys(channel))


def pub_event(channel: str, event: dict) -> None:
    """
    publish events to channel
    :param channel: channel name
    :param event: event dict
    """
    redis_client.xadd(channel, event)
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
