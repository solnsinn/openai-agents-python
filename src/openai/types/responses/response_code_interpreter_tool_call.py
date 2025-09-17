from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    class ResponseCodeInterpreterToolCall(BaseModel):
        """Minimal pydantic-friendly stub used for local imports/tests."""

        code: Optional[str] = None
        output: Optional[Any] = None

except Exception:
    class ResponseCodeInterpreterToolCall:
        def __init__(self, code: Any = None, output: Any = None):
            self.code = code
            self.output = output

__all__ = ["ResponseCodeInterpreterToolCall"]
