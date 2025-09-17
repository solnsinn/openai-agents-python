from __future__ import annotations

from openai.types.chat._shim_base import AttrDict


class Choice(AttrDict):
    pass


class ChoiceDelta(AttrDict):
    pass


class ChoiceDeltaToolCall(AttrDict):
    pass


class ChoiceDeltaToolCallFunction(ChoiceDeltaToolCall):
    pass


class ChatCompletionChunk(AttrDict):
    pass


__all__ = ["ChatCompletionChunk", "Choice", "ChoiceDelta"]
