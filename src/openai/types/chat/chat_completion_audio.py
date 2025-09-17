from typing import TypedDict, Optional


class ChatCompletionAudio(TypedDict, total=False):
    url: Optional[str]
    mime_type: Optional[str]


__all__ = ["ChatCompletionAudio"]
