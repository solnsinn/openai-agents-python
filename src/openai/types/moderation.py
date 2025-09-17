"""Moderation types shim used by third-party imports."""
from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "Moderation",
    "Categories",
    "CategoryAppliedInputTypes",
    "CategoryScores",
]


class Categories(BaseModel):
    hate: bool
    harassment: bool
    sexual: bool


class CategoryAppliedInputTypes(BaseModel):
    harassment: List[Literal["text"]]
    harassment_threatening: List[Literal["text"]]
    hate: List[Literal["text"]]
    hate_threatening: List[Literal["text"]]
    illicit: List[Literal["text"]]
    illicit_violent: List[Literal["text"]]
    self_harm: List[Literal["text", "image"]]
    self_harm_instructions: List[Literal["text", "image"]]
    self_harm_intent: List[Literal["text", "image"]]
    sexual: List[Literal["text", "image"]]
    sexual_minors: List[Literal["text"]]
    violence: List[Literal["text", "image"]]
    violence_graphic: List[Literal["text", "image"]]


class CategoryScores(BaseModel):
    harassment: float
    harassment_threatening: float
    hate: float
    hate_threatening: float
    illicit: float
    illicit_violent: float
    self_harm: float
    self_harm_instructions: float
    self_harm_intent: float
    sexual: float
    sexual_minors: float
    violence: float
    violence_graphic: float


class Moderation(BaseModel):
    categories: Categories
    category_applied_input_types: CategoryAppliedInputTypes
    category_scores: CategoryScores
    flagged: bool

