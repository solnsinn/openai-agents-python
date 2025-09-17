"""Helpers for responses shim: attribute-accessible container used by stubs."""

from __future__ import annotations

from typing import Any

try:
    from pydantic import BaseModel

    class AttrDict(BaseModel):
        model_config = {"extra": "allow", "arbitrary_types_allowed": True}

        def __init__(self, **data: Any) -> None:  # type: ignore[override]
            # Let pydantic handle initialization but accept arbitrary fields.
            super().__init__(**data)

        def __repr__(self) -> str:  # pragma: no cover - trivial
            return f"{self.__class__.__name__}({self.model_dump()})"
except Exception:
    class AttrDict:
        def __init__(self, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)

        def __repr__(self) -> str:  # pragma: no cover - trivial
            return f"{self.__class__.__name__}({self.__dict__})"

            def __getattr__(self, item: str) -> Any:  # pragma: no cover - defensive
                return None
