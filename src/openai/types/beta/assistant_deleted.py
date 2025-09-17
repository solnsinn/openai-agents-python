from typing import TypedDict, Optional


class AssistantDeleted(TypedDict, total=False):
    id: Optional[str]
    deleted: Optional[bool]


__all__ = ["AssistantDeleted"]
