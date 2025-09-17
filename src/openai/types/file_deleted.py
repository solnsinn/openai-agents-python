from typing import TypedDict, Optional


class FileDeleted(TypedDict, total=False):
    id: Optional[str]
    deleted: Optional[bool]


__all__ = ["FileDeleted"]
