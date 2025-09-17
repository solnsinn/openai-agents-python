"""Shim for InputAudioBufferAppendEvent used by realtime code."""
from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class InputAudioBufferAppendEvent(BaseModel):
        type: Optional[str] = None
        audio: Optional[str] = None
        audio_format: Optional[str] = None

except Exception:
    class InputAudioBufferAppendEvent:
        def __init__(self, type: Any = None, audio: Any = None, audio_format: Any = None):
            self.type = type
            self.audio = audio
            self.audio_format = audio_format


__all__ = ["InputAudioBufferAppendEvent"]
