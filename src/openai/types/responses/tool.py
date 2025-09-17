from typing import TypedDict, Optional


class Tool(TypedDict, total=False):
    name: str
    description: Optional[str]


__all__ = ["Tool"]
