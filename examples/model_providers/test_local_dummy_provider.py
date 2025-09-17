"""Standalone runner for the local DummyProvider.

This file intentionally does not use pytest so it can be run directly and avoids
loading `tests/conftest.py` which imports package-level test helpers.
"""
import asyncio
import sys

from agents.items import ModelResponse


async def _run():
    from examples.model_providers.local_dummy_provider import DummyProvider

    provider = DummyProvider()
    model = provider.get_model(None)

    resp = await model.get_response(
        system_instructions=None,
        input="Hello",
        model_settings=None,
        tools=[],
        output_schema=None,
        handoffs=[],
        tracing=None,
        previous_response_id=None,
        prompt=None,
    )

    assert isinstance(resp, ModelResponse), f"Expected ModelResponse, got {type(resp)}"
    assert resp.response_id == "local-1"
    assert len(resp.output) == 1
    print("DummyProvider test runner: OK")


if __name__ == "__main__":
    try:
        asyncio.run(_run())
    except AssertionError as e:
        print("Assertion failed:", e)
        sys.exit(2)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)