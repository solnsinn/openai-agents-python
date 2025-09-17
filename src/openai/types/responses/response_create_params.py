from typing import TypedDict, Optional, List, Any

from .response_includable import ResponseIncludable
from .response_input_param import ResponseInputParam


class Reasoning(TypedDict, total=False):
    encrypted_content: Optional[str]


class ToolChoice(TypedDict, total=False):
    type: Optional[str]


class ResponseCreateParamsBase(TypedDict, total=False):
    input: Any  # could be str or ResponseInputParam
    instructions: Optional[str]
    include: Optional[List[ResponseIncludable]]


class ToolParam(TypedDict, total=False):
    name: Optional[str]
    description: Optional[str]


# ResponseInputParam is also sometimes imported from here by upstream code; re-export
ToolParamAlias = ToolParam

__all__ = [
    "Reasoning",
    "ToolChoice",
    "ResponseCreateParamsBase",
    "ResponseIncludable",
    "ToolParam",
    "ToolParamAlias",
]
