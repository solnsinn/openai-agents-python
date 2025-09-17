from typing import TypedDict, Any


class Message(TypedDict, total=False):
    id: str
    role: str
    content: Any


__all__ = ["Message"]
