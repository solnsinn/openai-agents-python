from typing import TypedDict, List, Any


class Embedding(TypedDict, total=False):
    object: str
    data: List[Any]
    model: str
    usage: dict


__all__ = ["Embedding"]
