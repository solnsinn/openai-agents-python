import pytest
from pydantic import BaseModel
from agents.model_settings import ModelSettings

def test_resolve_returns_self_when_override_none():
    s = ModelSettings(temperature=0.1, top_p=0.2)
    returned = s.resolve(None)
    assert returned is s
    assert returned.temperature == 0.1
    assert returned.top_p == 0.2


def test_resolve_overrides_and_merges_extra_args():
    base = ModelSettings(
        temperature=0.1,
        presence_penalty=0.0,
        extra_args={"a": 1, "shared": "base"},
    )
    override = ModelSettings(
        temperature=0.5,
        frequency_penalty=0.3,
        extra_args={"b": 2, "shared": "override"},
    )

    resolved = base.resolve(override)

    # scalar overrides
    assert resolved.temperature == 0.5
    assert resolved.frequency_penalty == 0.3
    # unchanged if not provided by override
    assert resolved.presence_penalty == 0.0

    # extra_args merged with override taking precedence for shared keys
    assert resolved.extra_args == {"a": 1, "shared": "override", "b": 2}


def test_resolve_empty_dicts_become_none():
    base = ModelSettings(extra_args={})
    override = ModelSettings(extra_args={})
    resolved = base.resolve(override)
    # when both are empty dicts, combined result should be None per implementation
    assert resolved.extra_args is None


def test_to_json_dict_converts_pydantic_base_model_field():
    class Dummy(BaseModel):
        x: int

    dummy = Dummy(x=123)
    # assign dummy to a field (reasoning is annotated but dataclass is not runtime enforcing)
    s = ModelSettings(temperature=0.7, reasoning=dummy)

    json_dict = s.to_json_dict()
    # reasoning should be converted via model_dump
    assert "reasoning" in json_dict
    assert json_dict["reasoning"] == {"x": 123}
    # other fields preserved
    assert json_dict["temperature"] == 0.7