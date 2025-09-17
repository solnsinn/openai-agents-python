from enum import Enum


class ChatCompletionModality(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


__all__ = ["ChatCompletionModality"]
