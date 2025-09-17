"""Shim for realtime assistant message content using BaseModel at runtime."""
from __future__ import annotations

from typing import List, Optional, Any

try:
    from pydantic import BaseModel

    class Content(BaseModel):
        type: Optional[str] = None
        text: Optional[str] = None

    class RealtimeConversationItemAssistantMessage(BaseModel):
        id: Optional[str] = None
        type: Optional[str] = None
        role: Optional[str] = None
        content: Optional[list[Content]] = None

except Exception:
    class Content:
        def __init__(self, type: Any = None, text: Any = None):
            self.type = type
            self.text = text

    class RealtimeConversationItemAssistantMessage:
        def __init__(self, id: Any = None, type: Any = None, role: Any = None, content: Any = None):
            self.id = id
            self.type = type
            self.role = role
            self.content = content

__all__ = ["RealtimeConversationItemAssistantMessage", "Content"]
