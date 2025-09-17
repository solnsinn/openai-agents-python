from __future__ import annotations

from typing import TypedDict, Any


class ResponseFormat(TypedDict, total=False):
    type: str
    json_schema: Any


__all__ = ["ResponseFormat"]


class CompletionCreateParamsNonStreaming(TypedDict, total=False):
    model: str
    messages: Any
    max_tokens: Any
    temperature: Any


class CompletionCreateParamsStreaming(CompletionCreateParamsNonStreaming):
    stream: bool


__all__.extend(["CompletionCreateParamsNonStreaming", "CompletionCreateParamsStreaming"])
