"""Stub for ResponseFunctionToolCall used by the project.

Provide a small pydantic-friendly class rather than a TypedDict so
runtime isinstance checks and pydantic validation behave as tests expect.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel
    from .response import ResponseOutputItem


    class ResponseFunctionToolCall(ResponseOutputItem, BaseModel):
        name: Optional[str] = None
        arguments: Optional[Any] = None
        call_id: Optional[str] = None

except Exception:
    from .response import ResponseOutputItem  # type: ignore


    class ResponseFunctionToolCall(ResponseOutputItem):
        def __init__(self, name: Any = None, arguments: Any = None, call_id: Any = None):
            self.name = name
            self.arguments = arguments
            self.call_id = call_id


__all__ = ["ResponseFunctionToolCall"]
