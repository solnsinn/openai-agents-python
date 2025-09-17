from __future__ import annotations

from typing import TypedDict, Any, List, Dict


class ChatCompletionToolParam(TypedDict, total=False):
    name: str
    description: str
    parameters: Dict[str, Any]


__all__ = ["ChatCompletionToolParam"]
