from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class Filters(BaseModel):
        query: Optional[str] = None

except Exception:
    class Filters:
        def __init__(self, query: Any = None):
            self.query = query

__all__ = ["Filters"]
