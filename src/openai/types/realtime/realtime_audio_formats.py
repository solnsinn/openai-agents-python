"""Realtime audio formats shim used by tests.

Provides pydantic-friendly classes for audio formats so runtime checks
and schema generation work in the tests.
"""
from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class AudioPCM(BaseModel):
        type: Optional[str] = None
        rate: Optional[int] = None

    class AudioPCMU(BaseModel):
        type: Optional[str] = None

    class AudioPCMA(BaseModel):
        type: Optional[str] = None

except Exception:
    class AudioPCM:
        def __init__(self, type: Any = None, rate: Any = None):
            self.type = type
            self.rate = rate

    class AudioPCMU:
        def __init__(self, type: Any = None):
            self.type = type

    class AudioPCMA:
        def __init__(self, type: Any = None):
            self.type = type

RealtimeAudioFormats = (AudioPCM, AudioPCMU, AudioPCMA)

__all__ = ["AudioPCM", "AudioPCMU", "AudioPCMA", "RealtimeAudioFormats"]
