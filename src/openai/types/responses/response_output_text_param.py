"""Minimal stub for ResponseOutputTextParam used in tests.

Provide a simple, pydantic-friendly class with attribute access and mapping
semantics similar to other response shims.
"""
from __future__ import annotations

from typing import Any


class ResponseOutputTextParam(dict):
    """Dict-like shim used by tests; keeps keys in insertion order for JSON output."""

    def __init__(self, *, type: Any | None = None, text: Any | None = None, annotations: Any | None = None):
        super().__init__()
        # Insert keys in the expected order
        self["type"] = type
        self["text"] = text
        self["annotations"] = annotations


__all__ = ["ResponseOutputTextParam"]


__all__ = ["ResponseOutputTextParam"]
