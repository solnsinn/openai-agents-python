"""Shim for a realtime conversation user message.

Provide a pydantic BaseModel so runtime code can perform isinstance
checks and attribute access as expected by the test-suite.
"""
from __future__ import annotations

from typing import List, Optional

try:
    from pydantic import BaseModel

    class Content(BaseModel):
        type: Optional[str] = None
        text: Optional[str] = None

    class RealtimeConversationItemUserMessage(BaseModel):
        id: Optional[str] = None
        type: Optional[str] = None
        role: Optional[str] = None
        content: Optional[List[Content]] = None

except Exception:
    class Content:
        def __init__(self, type: str | None = None, text: str | None = None):
            self.type = type
            self.text = text

    class RealtimeConversationItemUserMessage:
        def __init__(self, id: str | None = None, type: str | None = None, role: str | None = None, content: list | None = None):
            self.id = id
            self.type = type
            self.role = role
            self.content = content


__all__ = ["RealtimeConversationItemUserMessage", "Content"]
