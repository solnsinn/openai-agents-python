from typing_extensions import TypedDict


class ChatCompletionContentPartTextParam(TypedDict, total=False):
    text: str


__all__ = ["ChatCompletionContentPartTextParam"]
