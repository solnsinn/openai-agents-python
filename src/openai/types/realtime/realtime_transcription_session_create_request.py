"""Realtime transcription session create request shim used by tests."""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class RealtimeTranscriptionSessionCreateRequest(BaseModel):
    # Minimal fields used by tests; presence of this class enables isinstance checks.
    type: Optional[str] = None
    model: Optional[str] = None
    audio: Optional[Any] = None


__all__ = ["RealtimeTranscriptionSessionCreateRequest"]
