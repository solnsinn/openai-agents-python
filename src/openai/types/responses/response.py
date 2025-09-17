"""Stub for Response type used by codebase (attribute-accessible)."""
from __future__ import annotations

from openai.types.responses._shim_base import AttrDict
from typing import List, Optional, TYPE_CHECKING, Any

if TYPE_CHECKING:
    # Import for type checkers only to avoid runtime circular imports.
    from openai.types.responses.tool import Tool
else:
    # At runtime, import Tool from the local responses.tool module so upstream
    # packages that expect `from openai.types.responses.response import Tool`
    # succeed.
    try:
        from openai.types.responses.tool import Tool  # type: ignore
    except Exception:
        # Fallback minimal runtime stub
        class Tool:  # pragma: no cover - defensive
            pass


class ResponseOutputItem(AttrDict):
    pass


class IncompleteDetails(AttrDict):
    reason: Optional[str] = None


class Response(AttrDict):
    id: str | None = None
    created_at: float | None = None
    incomplete_details: Optional[IncompleteDetails] = None
    # Be permissive about output item types: tests and local stubs may produce
    # BaseModel instances or simple dict-like objects. Using Any here avoids
    # pydantic attempting strict instance checks against a potentially
    # different ResponseOutputItem class object coming from another module.
    output: List[Any] | None = None



class ToolChoice(AttrDict):
    pass


__all__ = ["Response", "IncompleteDetails", "ResponseOutputItem", "Tool", "ToolChoice"]
