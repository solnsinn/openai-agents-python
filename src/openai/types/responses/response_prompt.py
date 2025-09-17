from __future__ import annotations

from typing import TypedDict, Any


class ResponsePrompt(TypedDict, total=False):
    text: str
    tokens: list[Any]


__all__ = ["ResponsePrompt"]
