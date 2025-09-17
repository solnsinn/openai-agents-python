"""Small helper shim used by chat type stubs to provide attribute access.

These are intentionally simple: they accept any kwargs and set them as
attributes so tests can construct nested objects like Choice(...)
and access fields with dot-notation.
"""

from __future__ import annotations

from typing import Any


class AttrDict:
    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"{self.__class__.__name__}({self.__dict__})"

    def __getattr__(self, item: str) -> Any:  # pragma: no cover - defensive
        # Return None for missing attributes to behave like dict.get(key)
        # This keeps code that does `if delta.tool_calls:` safe when the
        # field isn't present on the shim object.
        return None

    # Mapping-like access so objects can be used as dicts in tests
    def __getitem__(self, key: str) -> Any:  # pragma: no cover - defensive
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        # Allow dict-style assignment to the AttrDict-backed objects used in tests
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        if hasattr(self, key):
            delattr(self, key)
        else:
            raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:  # pragma: no cover - defensive
        return getattr(self, key, default)

    def keys(self):  # pragma: no cover - defensive
        return list(self.__dict__.keys())

    def items(self):  # pragma: no cover - defensive
        return list(self.__dict__.items())

    def __iter__(self):  # pragma: no cover - defensive
        return iter(self.__dict__)

    def __len__(self):  # pragma: no cover - defensive
        return len(self.__dict__)

    def __contains__(self, key: object) -> bool:  # pragma: no cover - defensive
        return key in self.__dict__
