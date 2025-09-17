from typing import TypedDict, Any


class AssistantToolParam(TypedDict, total=False):
    name: str
    description: str
    schema: dict[str, Any]


__all__ = ["AssistantToolParam"]
