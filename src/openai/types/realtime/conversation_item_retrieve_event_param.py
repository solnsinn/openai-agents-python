"""Parameter types for ConversationItemRetrieveEvent."""
from typing import TypedDict, Optional


class ConversationItemRetrieveEventParam(TypedDict, total=False):
    item_id: str
    type: str
    event_id: Optional[str]


__all__ = ["ConversationItemRetrieveEventParam"]
