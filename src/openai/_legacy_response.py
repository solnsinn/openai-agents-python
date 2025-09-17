"""Minimal legacy response shim for third-party imports (litellm)."""
from typing import TypedDict, List, Any


class ChatCompletionChoice(TypedDict, total=False):
    index: int
    message: dict
    finish_reason: str


class ChatCompletion(TypedDict, total=False):
    id: str
    object: str
    choices: List[ChatCompletionChoice]


class Response(TypedDict, total=False):
    id: str
    model: str
    choices: List[dict]


__all__ = ["ChatCompletion", "ChatCompletionChoice", "Response"]


# httpx binary response content shim used by some upstream libraries
class HttpxBinaryResponseContent(TypedDict, total=False):
    content: bytes

__all__.append("HttpxBinaryResponseContent")
