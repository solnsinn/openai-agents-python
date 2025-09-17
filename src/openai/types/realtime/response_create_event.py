from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class ResponseCreateEvent(BaseModel):
        type: Optional[str] = None
        id: Optional[str] = None
        output: Optional[Any] = None

except Exception:
    class ResponseCreateEvent:
        def __init__(self, type: Any = None, id: Any = None, output: Any = None):
            self.type = type
            self.id = id
            self.output = output


__all__ = ["ResponseCreateEvent"]
