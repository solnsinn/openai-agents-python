from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    class Filters(BaseModel):
        query: Optional[str] = None


    class RankingOptions(BaseModel):
        strategy: Optional[str] = None
        top_k: Optional[int] = None

except Exception:
    class Filters:
        def __init__(self, query: Any = None):
            self.query = query


    class RankingOptions:
        def __init__(self, strategy: Any = None, top_k: Any = None):
            self.strategy = strategy
            self.top_k = top_k

__all__ = ["Filters", "RankingOptions"]
