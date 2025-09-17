from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class SessionUpdateEvent(BaseModel):
        type: Optional[str] = None
        session: Optional[Any] = None

except Exception:
    class SessionUpdateEvent:
        def __init__(self, type: Any = None, session: Any = None):
            self.type = type
            self.session = session


__all__ = ["SessionUpdateEvent"]
