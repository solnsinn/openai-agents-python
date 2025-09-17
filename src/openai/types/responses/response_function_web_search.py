"""Stub for response function web search actions used in tests.

Provide class-based shims instead of TypedDicts so runtime isinstance
checks work and pydantic validation treats instances as model objects.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel
    class ActionSearch(BaseModel):
        type: Optional[str] = "search"
        query: Optional[str] = None
        num_results: Optional[int] = None


    class ResponseFunctionWebSearch(BaseModel):
        id: Optional[str] = None
        action: Optional[ActionSearch] = None
        status: Optional[str] = None
        type: Optional[str] = None


    class ResponseFunctionWebSearchParam(BaseModel):
        query: Optional[str] = None
        num_results: Optional[int] = None
except Exception:
    class ActionSearch:
        def __init__(self, query: Any = None, num_results: Any = None, type: Any = "search"):
            self.type = type
            self.query = query
            self.num_results = num_results


    class ResponseFunctionWebSearch:
        def __init__(self, id: Any = None, action: Any = None, status: Any = None, type: Any = None):
            self.id = id
            self.action = action
            self.status = status
            self.type = type


    class ResponseFunctionWebSearchParam:
        def __init__(self, query: Any = None, num_results: Any = None):
            self.query = query
            self.num_results = num_results


__all__ = ["ActionSearch", "ResponseFunctionWebSearch", "ResponseFunctionWebSearchParam"]
