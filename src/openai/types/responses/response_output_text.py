from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    class ResponseOutputText(BaseModel):
        type: Optional[str] = None
        text: Optional[str] = None
        annotations: Optional[list[Any]] = None

except Exception:
    class ResponseOutputText:
        def __init__(self, type: Any = None, text: Any = None, annotations: Any = None):
            self.type = type
            self.text = text
            self.annotations = annotations


__all__ = ["ResponseOutputText"]
