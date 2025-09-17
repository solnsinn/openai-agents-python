"""Param shim for ResponseFunctionWebSearchParam."""
from typing import TypedDict


class ResponseFunctionWebSearchParam(TypedDict, total=False):
    query: str
    num_results: int


__all__ = ["ResponseFunctionWebSearchParam"]
