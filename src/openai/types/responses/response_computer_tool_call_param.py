"""Stub for ResponseComputerToolCallParam used in tests."""
from typing import TypedDict, Any


class ResponseComputerToolCallParam(TypedDict, total=False):
    name: str
    output: Any


__all__ = ["ResponseComputerToolCallParam"]
