"""Shim for function call output in realtime conversation items."""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class RealtimeConversationItemFunctionCallOutput(BaseModel):
    type: Optional[str] = None
    output: Optional[Any] = None
    # call_id is required by tests; None should raise a ValidationError
    call_id: str
    name: Optional[str] = None
    arguments: Optional[Any] = None


__all__ = ["RealtimeConversationItemFunctionCallOutput"]
