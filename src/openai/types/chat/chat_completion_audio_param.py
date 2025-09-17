from typing import TypedDict, Any


class ChatCompletionAudioParam(TypedDict, total=False):
    format: str
    sample_rate: int
    channels: int


__all__ = ["ChatCompletionAudioParam"]
