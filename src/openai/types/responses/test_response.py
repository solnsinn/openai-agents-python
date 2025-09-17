import importlib

import pytest

# ...existing imports...
from openai.types.responses.response import (
    Response,
    IncompleteDetails,
    ResponseOutputItem,
    ToolChoice,
)


def test_response_defaults():
    r = Response()
    assert r.id is None
    assert r.created_at is None
    assert r.incomplete_details is None
    assert r.output is None


def test_attribute_and_item_access():
    r = Response()
    r.id = "r1"
    r["created_at"] = 1.23
    r.incomplete_details = IncompleteDetails(reason="timeout")

    assert r["id"] == "r1"
    assert r.created_at == 1.23
    assert isinstance(r.incomplete_details, IncompleteDetails)
    assert r.incomplete_details.reason == "timeout"


def test_incomplete_details_mutation():
    inc = IncompleteDetails()
    assert inc.reason is None
    inc.reason = "error"
    assert inc["reason"] == "error"


def test_output_and_output_items():
    item = ResponseOutputItem()
    item.type = "message"
    item.content = "hello"

    r = Response(output=[item])
    assert isinstance(r.output, list)
    assert r.output[0].type == "message"
    assert r.output[0]["content"] == "hello"


def test_toolchoice_basic():
    t = ToolChoice()
    t.name = "tool1"
    assert t["name"] == "tool1"
    assert getattr(t, "name") == "tool1"


def test_module_all_contains_expected_names():
    mod = importlib.import_module("openai.types.responses.response")
    expected = {"Response", "IncompleteDetails", "ResponseOutputItem", "Tool", "ToolChoice"}
    assert set(getattr(mod, "__all__", [])) == expected
