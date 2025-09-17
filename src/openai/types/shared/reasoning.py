"""Stub for openai.types.shared.reasoning.Reasoning used by the codebase."""
from typing import TypedDict, Any

class Reasoning(TypedDict, total=False):
    explanation: str
    score: float

__all__ = ["Reasoning"]
