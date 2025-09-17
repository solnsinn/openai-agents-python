"""Minimal chat.chat_completion shim providing attribute access."""
from typing import Any

from openai.types.chat._shim_base import AttrDict


class Choice(AttrDict):
	pass


class ChatCompletion(AttrDict):
	pass


__all__ = ["Choice", "ChatCompletion"]

