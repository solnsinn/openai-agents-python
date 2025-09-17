"""Stub for ResponseOutputMessage used by the project.

Provide a small pydantic-friendly class rather than a TypedDict so
runtime isinstance checks and pydantic validation behave as tests expect.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    # Import the ResponseOutputItem shim so message/tool classes are accepted
    # wherever a ResponseOutputItem is expected by pydantic validators.
    from .response import ResponseOutputItem


    class ResponseOutputMessage(ResponseOutputItem, BaseModel):
        id: Optional[str] = None
        type: Optional[str] = None
        role: Optional[str] = None
        content: Optional[Any] = None

except Exception:
    # Fallback minimal runtime class that mirrors the fields used in tests.
    from .response import ResponseOutputItem  # type: ignore


    class ResponseOutputMessage(ResponseOutputItem):
        def __init__(self, id: Any = None, type: Any = None, role: Any = None, content: Any = None):
            self.id = id
            self.type = type
            self.role = role
            self.content = content


__all__ = ["ResponseOutputMessage"]
