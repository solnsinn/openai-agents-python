"""Stub for ResponseFileSearchToolCall used by the project.

Provide a small pydantic-friendly class rather than a TypedDict so
runtime isinstance checks and pydantic validation behave as tests expect.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    class ResponseFileSearchToolCall(BaseModel):
        id: Optional[str] = None
        queries: Optional[list[Any]] = None
        status: Optional[str] = None
        type: Optional[str] = None
        results: Optional[Any] = None

except Exception:
    class ResponseFileSearchToolCall:
        def __init__(self, id: Any = None, queries: Any = None, status: Any = None, type: Any = None, results: Any = None):
            self.id = id
            self.queries = queries
            self.status = status
            self.type = type
            self.results = results


__all__ = ["ResponseFileSearchToolCall"]
