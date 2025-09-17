from typing import TypedDict, Any


class MessageContent(TypedDict, total=False):
    type: str
    text: str
    parts: list[Any]


__all__ = ["MessageContent"]
