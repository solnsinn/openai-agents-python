"""Realtime audio config shim used by tests and agent code.

Provide Pydantic models with `input`/`output` sub-configs to match the
expectations in tests and in the agent implementation.
"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class RealtimeAudioConfigInput(BaseModel):
    # Format is an arbitrary OpenAI audio format model or string; keep permissive
    format: Optional[Any] = None
    transcription: Optional[Any] = None
    turn_detection: Optional[Any] = None


class RealtimeAudioConfigOutput(BaseModel):
    format: Optional[Any] = None
    speed: Optional[Any] = None
    voice: Optional[str] = None


class RealtimeAudioConfig(BaseModel):
    input: Optional[RealtimeAudioConfigInput] = None
    output: Optional[RealtimeAudioConfigOutput] = None


__all__ = [
    "RealtimeAudioConfig",
    "RealtimeAudioConfigInput",
    "RealtimeAudioConfigOutput",
]
