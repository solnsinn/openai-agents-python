from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    class ResponseOutputRefusal(BaseModel):
        type: Optional[str] = None
        refusal: Optional[str] = None

except Exception:
    class ResponseOutputRefusal:
        def __init__(self, type: Any = None, refusal: Any = None):
            self.type = type
            self.refusal = refusal


__all__ = ["ResponseOutputRefusal"]
