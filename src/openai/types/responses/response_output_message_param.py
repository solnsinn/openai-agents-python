from __future__ import annotations

from typing import Any


class ResponseOutputMessageParam(dict):
    """A minimal dict-like shim to behave like the upstream TypedDict so json.dumps works."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


__all__ = ["ResponseOutputMessageParam"]
