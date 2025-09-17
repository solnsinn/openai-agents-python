"""Shim for openai.types.responses used in repository imports."""
from typing import TypedDict, Any

class ResponseData(TypedDict, total=False):
    content: Any


class ResponseIncludable(TypedDict, total=False):
    include: bool

__all__ = ['ResponseData', 'ResponseIncludable']
