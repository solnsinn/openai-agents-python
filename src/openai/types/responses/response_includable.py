"""Stub for ResponseIncludable used in the repo."""
from typing import TypedDict, Any

from openai.types.responses._shim_base import AttrDict

class ResponseIncludable(AttrDict):
    pass

__all__ = ['ResponseIncludable']
