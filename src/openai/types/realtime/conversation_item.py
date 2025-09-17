"""Shim for openai.types.realtime.conversation_item used by tests and code.

Define ConversationItem and a Content type union expected by the code that
imports `Content` from realtime conversation item modules.
"""
from typing import TypedDict, Union, Any


class ConversationItem(TypedDict, total=False):
    id: str
    type: str
    content: dict


# Content is a union alias used elsewhere when importing `Content`.
Content = dict[str, Any]


__all__ = ["ConversationItem", "Content"]
