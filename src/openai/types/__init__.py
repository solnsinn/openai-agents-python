"""openai.types package shim"""
from dataclasses import dataclass
from typing import TypedDict, Any

# expose subpackages
from . import shared


@dataclass
class ChatModel:
	id: str
	name: str | None = None


class Batch(TypedDict, total=False):
	items: list[Any]


class EmbeddingCreateParams(TypedDict, total=False):
	input: Any
	model: str | None


class FileObject(TypedDict, total=False):
	id: str
	filename: str
	bytes: bytes


__all__ = [
	"shared",
	"ChatModel",
	"Batch",
	"EmbeddingCreateParams",
	"FileObject",
]
