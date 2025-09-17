from __future__ import annotations

from typing import TypedDict, Any, List, Dict


class FunctionCallOutput(TypedDict, total=False):
    type: str
    arguments: Dict[str, Any]


class ItemReference(TypedDict, total=False):
    type: str
    id: str


class Message(TypedDict, total=False):
    type: str
    role: str
    content: Any



class ComputerCallOutput(TypedDict, total=False):
    output: Any


class McpApprovalResponse(TypedDict, total=False):
    approved: bool
    reason: str


__all__ = [
    "FunctionCallOutput",
    "ItemReference",
    "Message",
    "ComputerCallOutput",
    "McpApprovalResponse",
]

# Upstream name alias used by some consumers
ResponseInputParam = Message
__all__.append("ResponseInputParam")
