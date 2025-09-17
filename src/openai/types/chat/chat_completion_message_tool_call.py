from __future__ import annotations

from typing import Any

from openai.types.chat._shim_base import AttrDict


class Function(AttrDict):
    pass


class ChatCompletionMessageFunctionToolCall(AttrDict):
    pass


__all__ = ["ChatCompletionMessageFunctionToolCall", "Function"]
