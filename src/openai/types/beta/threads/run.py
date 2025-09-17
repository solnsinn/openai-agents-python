from typing import TypedDict, Any


class Run(TypedDict, total=False):
    id: str
    type: str
    content: Any


__all__ = ["Run"]
