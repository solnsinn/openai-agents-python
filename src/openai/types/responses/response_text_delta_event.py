from __future__ import annotations

from typing import Any, Optional

from openai.types.responses._shim_base import AttrDict


class ResponseTextDeltaEvent(AttrDict):
    """Attribute-accessible shim for response text delta events."""


__all__ = ["ResponseTextDeltaEvent"]
