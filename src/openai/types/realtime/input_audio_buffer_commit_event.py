"""Shim for InputAudioBufferCommitEvent used by realtime code."""
from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class InputAudioBufferCommitEvent(BaseModel):
        type: Optional[str] = None
        audio: Optional[str] = None

except Exception:
    class InputAudioBufferCommitEvent:
        def __init__(self, type: Any = None, audio: Any = None):
            self.type = type
            self.audio = audio


__all__ = ["InputAudioBufferCommitEvent"]
