"""Shim for moderation create response used by third-party libs."""
from typing import TypedDict

from .moderation import Moderation


class ModerationCreateResponse(TypedDict, total=False):
    id: str
    model: str
    results: list[Moderation]


__all__ = ["ModerationCreateResponse"]
