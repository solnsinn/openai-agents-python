"""Shim for realtime function tool types used by the agents code."""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class RealtimeFunctionTool(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[dict[str, Any]] = None
    type: Optional[str] = "function"


__all__ = ["RealtimeFunctionTool"]
