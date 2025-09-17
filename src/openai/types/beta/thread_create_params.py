from typing import TypedDict, Any


class Message(TypedDict, total=False):
    role: str
    content: Any


class ThreadCreateParams(TypedDict, total=False):
    title: str
    body: Any
    Message: Message  # included for compatibility


__all__ = ["ThreadCreateParams", "Message"]
