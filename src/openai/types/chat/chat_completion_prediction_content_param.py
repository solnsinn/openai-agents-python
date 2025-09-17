from typing import Iterable, Union
from typing_extensions import TypedDict, Literal

from openai.types.chat.chat_completion_content_part_text_param import (
    ChatCompletionContentPartTextParam,
)


class ChatCompletionPredictionContentParam(TypedDict, total=False):
    content: Union[str, Iterable[ChatCompletionContentPartTextParam]]
    type: Literal["content"]


__all__ = ["ChatCompletionPredictionContentParam"]
