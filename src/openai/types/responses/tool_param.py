from __future__ import annotations

from typing import Optional, TypedDict


class CodeInterpreter(TypedDict, total=False):
    enabled: Optional[bool]


class ImageGeneration(TypedDict, total=False):
    size: Optional[str]


class Mcp(TypedDict, total=False):
    id: Optional[str]


class FunctionToolParam(TypedDict, total=False):
    name: str
    description: Optional[str]
    parameters: Optional[dict]


__all__ = ["CodeInterpreter", "ImageGeneration", "Mcp", "FunctionToolParam"]
