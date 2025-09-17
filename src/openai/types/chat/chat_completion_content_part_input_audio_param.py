from typing import TypedDict, Any


class ChatCompletionContentPartInputAudioParam(TypedDict, total=False):
    format: str
    sample_rate: int
    channels: int
    bytes: bytes


__all__ = ["ChatCompletionContentPartInputAudioParam"]
