"""Shim for RealtimeClientEvent used in realtime imports.

Make the `type` field permissive (str) so tests that validate many
server/client event variants can parse messages without requiring full
upstream schema fidelity.
"""
from typing import Optional

from ..._models import BaseModel

__all__ = ["RealtimeClientEvent"]


class RealtimeClientEvent(BaseModel):
    type: str
    event_id: Optional[str] = None
