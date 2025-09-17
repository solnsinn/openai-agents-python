"""Minimal shim for openai._models used by third-party packages during tests.

This provides tiny stand-ins for Model and ModelType names that some packages
import at collection time. Keep it minimal to avoid changing runtime behavior.
"""

from typing import Any

from pydantic import BaseModel as _PydanticBaseModel


# Provide a tiny Model shim
class Model:
    def __init__(self, **kwargs: Any):
        # accept arbitrary kwargs to be permissive
        self._data = kwargs

    def __repr__(self) -> str:  # pragma: no cover - tiny shim
        return f"Model({self._data!r})"


class ModelType:
    def __init__(self, name: str | None = None):
        self.name = name

    def __repr__(self) -> str:  # pragma: no cover - tiny shim
        return f"ModelType(name={self.name!r})"


# Some third-party code expects openai._models.BaseModel to be available.  Expose
# pydantic's BaseModel under that name so downstream imports succeed.
BaseModel = _PydanticBaseModel


__all__ = ["Model", "ModelType", "BaseModel"]
