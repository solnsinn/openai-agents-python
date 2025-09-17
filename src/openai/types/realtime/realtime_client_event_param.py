"""Parameter stub for RealtimeClientEvent."""
from typing import TypedDict, Optional


class RealtimeClientEventParam(TypedDict, total=False):
    type: str
    event_id: Optional[str]


__all__ = ["RealtimeClientEventParam"]
