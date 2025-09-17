"""Minimal chat types shim for tests/imports.
This provides attribute-accessible types referenced in the repository.
"""
from typing import Any, List, Optional

from openai.types.chat._shim_base import AttrDict


class ChatCompletionContentPartParam(AttrDict):
	pass


class ChatCompletionMessage(AttrDict):
	pass


class ChatCompletion(AttrDict):
	pass


class ChatCompletionChunk(AttrDict):
	pass


# Common param types used by the converter. Keep minimal shapes.
class ChatCompletionMessageParam(AttrDict):
	pass


class ChatCompletionUserMessageParam(ChatCompletionMessageParam):
	pass


class ChatCompletionSystemMessageParam(ChatCompletionMessageParam):
	pass


class ChatCompletionDeveloperMessageParam(ChatCompletionMessageParam):
	pass


class ChatCompletionAssistantMessageParam(ChatCompletionMessageParam):
	pass


class ChatCompletionContentPartTextParam(AttrDict):
	pass


class ChatCompletionContentPartImageParam(AttrDict):
	pass


class ChatCompletionMessageFunctionToolCallParam(AttrDict):
	pass


class ChatCompletionMessageFunctionToolCall(AttrDict):
	pass


# Some consumers import a CustomToolCall name; alias it to the function-tool call shim
ChatCompletionMessageCustomToolCall = ChatCompletionMessageFunctionToolCall


class ChatCompletionToolMessageParam(ChatCompletionMessageParam):
	pass


class ChatCompletionToolChoiceOptionParam(AttrDict):
	pass


__all__ = [
	"ChatCompletion",
	"ChatCompletionChunk",
	"ChatCompletionMessage",
	"ChatCompletionMessageParam",
	"ChatCompletionUserMessageParam",
	"ChatCompletionSystemMessageParam",
	"ChatCompletionDeveloperMessageParam",
	"ChatCompletionAssistantMessageParam",
	"ChatCompletionContentPartParam",
	"ChatCompletionContentPartTextParam",
	"ChatCompletionContentPartImageParam",
	"ChatCompletionMessageFunctionToolCallParam",
	"ChatCompletionToolMessageParam",
	"ChatCompletionToolChoiceOptionParam",
	"ChatCompletionMessageFunctionToolCall",
	"ChatCompletionMessageCustomToolCall",
]

