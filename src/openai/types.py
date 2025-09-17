"""Types shim for openai package used by this project."""
# Minimal types and helpers used in the repository; expand as needed.
from typing import TypedDict, Any, Dict

class ChatMessage(TypedDict):
    role: str
    content: str

class ChatCompletionChoice(TypedDict):
    message: ChatMessage

class ChatCompletion(TypedDict):
    choices: list[ChatCompletionChoice]

__all__ = ["ChatMessage", "ChatCompletion", "ChatCompletionChoice"]
