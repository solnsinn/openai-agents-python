# The line `"""Realtime session create request shim used by tests."""` is a docstring in Python.
# Docstrings are used to provide documentation for modules, classes, functions, or methods in Python
# code. In this case, the docstring is providing a brief description of the purpose of the module or
# class that follows it.
"""Realtime session create request shim used by tests."""
from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class _AudioConfig(BaseModel):
        input: Optional[Any] = None
        output: Optional[Any] = None

    class RealtimeSessionCreateRequest(BaseModel):
        model: Optional[str] = None
        type: Optional[str] = None
        audio: Optional[Any] = None
        tracing: Optional[Any] = None

except Exception:
    class RealtimeSessionCreateRequest:
        def __init__(self, model: Any = None, type: Any = None, audio: Any = None, tracing: Any = None):
            self.model = model
            self.type = type
            self.audio = audio
            self.tracing = tracing


__all__ = ["RealtimeSessionCreateRequest"]
