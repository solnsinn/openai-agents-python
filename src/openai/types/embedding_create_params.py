from typing import TypedDict, Optional, Any


class EmbeddingCreateParams(TypedDict, total=False):
    model: Optional[str]
    input: Any


__all__ = ["EmbeddingCreateParams"]
