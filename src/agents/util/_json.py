from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Literal

from pydantic import TypeAdapter, ValidationError
from typing_extensions import TypeVar

from ..exceptions import ModelBehaviorError
from ..tracing import SpanError
from ._error_tracing import attach_error_to_current_span

T = TypeVar("T")


def validate_json(json_str: str, type_adapter: TypeAdapter[T], partial: bool) -> T:
    partial_setting: bool | Literal["off", "on", "trailing-strings"] = (
        "trailing-strings" if partial else False
    )
    try:
        validated = type_adapter.validate_json(json_str, experimental_allow_partial=partial_setting)
        return validated
    except ValidationError as e:
        attach_error_to_current_span(
            SpanError(
                message="Invalid JSON provided",
                data={},
            )
        )
        raise ModelBehaviorError(
            f"Invalid JSON when parsing {json_str} for {type_adapter}; {e}"
        ) from e


def _to_dump_compatible(obj: Any) -> Any:
    return _to_dump_compatible_internal(obj)


def _to_dump_compatible_internal(obj: Any) -> Any:
    # Prefer actual dict/mapping handling first. Some shim types (AttrDict)
    # implement mapping-like methods but are not actual dicts. Treat any
    # Mapping or duck-typed object with an `items()` method as a mapping so
    # it will be converted to a JSON-dump-compatible dict rather than an
    # iterable (which would produce a list of values and break message
    # shapes).
    if isinstance(obj, dict):
        return {k: _to_dump_compatible_internal(v) for k, v in obj.items()}

    if isinstance(obj, Mapping):
        return {k: _to_dump_compatible_internal(v) for k, v in obj.items()}

    # Duck-typed mapping support for objects that expose `.items()` but don't
    # formally register Mapping as a base class (e.g., lightweight AttrDict
    # shims).
    # If it's a pydantic BaseModel or similar, try to call model_dump/model_dump_json
    # to obtain a mapping for serialization.
    if hasattr(obj, "model_dump") and callable(getattr(obj, "model_dump")):
        try:
            dumped = obj.model_dump(exclude_none=False, exclude_unset=False)
            if isinstance(dumped, Mapping):
                return {k: _to_dump_compatible_internal(v) for k, v in dumped.items()}
        except Exception:
            # ignore and continue to other handlers
            pass

    # Duck-typed mapping support for objects that expose `.items()` but don't
    # formally register Mapping as a base class (e.g., lightweight AttrDict
    # shims).
    if hasattr(obj, "items") and callable(getattr(obj, "items")):
        try:
            return {k: _to_dump_compatible_internal(v) for k, v in obj.items()}
        except Exception:
            # Fall through to iterable handling if `.items()` isn't usable.
            pass

    if isinstance(obj, (list, tuple)):
        return [_to_dump_compatible_internal(x) for x in obj]

    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes, bytearray)):
        return [_to_dump_compatible_internal(x) for x in obj]

    return obj
