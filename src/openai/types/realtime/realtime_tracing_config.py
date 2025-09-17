"""Realtime tracing configuration shim used by tests.

Provide TracingConfiguration (the real SDK name) and a backwards-compatible
alias so imports in this repo succeed.
"""
from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class TracingConfiguration(BaseModel):
        group_id: Optional[str] = None
        metadata: Optional[Any] = None
        workflow_name: Optional[str] = None

except Exception:
    class TracingConfiguration:
        def __init__(self, group_id: Any = None, metadata: Any = None, workflow_name: Any = None):
            self.group_id = group_id
            self.metadata = metadata
            self.workflow_name = workflow_name


# alias for older/alternate names
RealtimeTracingConfig = TracingConfiguration

__all__ = ["TracingConfiguration", "RealtimeTracingConfig"]
