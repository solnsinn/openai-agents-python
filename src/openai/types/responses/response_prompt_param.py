"""Stub for openai.types.responses.response_prompt_param.ResponsePromptParam and Variables"""
from typing import TypedDict, Any


class ResponsePromptParam(TypedDict, total=False):
    name: str
    value: Any


class Variables(TypedDict, total=False):
    # Represents arbitrary variables used in prompts. Keys are variable names.
    # Values are any JSON-serializable content.
    __root__: dict[str, Any]


__all__ = ["ResponsePromptParam", "Variables"]
