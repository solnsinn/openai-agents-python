from __future__ import annotations

from typing import TypedDict


class Part(TypedDict, total=False):
    text: str
    type: str


__all__ = ["Part"]
