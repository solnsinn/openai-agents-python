from __future__ import annotations

from typing import Any, Optional, TypedDict, List

try:
    from pydantic import BaseModel

    class Summary(BaseModel):
        text: str
        type: str

    class Content(BaseModel):
        text: str
        type: str

    class ResponseReasoningItem(BaseModel):
        id: Optional[str] = None
        type: Optional[str] = None
        reasoning: Optional[str] = None
        steps: Optional[list[Any]] = None
        summary: Optional[List[Summary]] = None
        content: Optional[List[Content]] = None

except Exception:
    class Summary(TypedDict, total=False):
        text: str
        type: str

    class Content(TypedDict, total=False):
        text: str
        type: str

    class ResponseReasoningItem:
        def __init__(self, id: Any = None, type: Any = None, reasoning: Any = None, steps: Any = None):
            self.id = id
            self.type = type
            self.reasoning = reasoning
            self.steps = steps
            self.summary = None
            self.content = None


__all__ = ["ResponseReasoningItem", "Summary", "Content"]
