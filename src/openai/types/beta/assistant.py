from typing import TypedDict, Any


class Assistant(TypedDict, total=False):
    id: str
    name: str
    metadata: dict[str, Any]


__all__ = ["Assistant"]
