from __future__ import annotations

from typing import Any

from openai.types.chat._shim_base import AttrDict


class ChatCompletionMessage(AttrDict):
    pass


# Placeholder Annotation type referenced by consumers
class Annotation(AttrDict):
    pass


class AnnotationURLCitation(Annotation):
    pass


__all__ = ["ChatCompletionMessage", "Annotation", "AnnotationURLCitation"]
