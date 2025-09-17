import pytest

from agents.items import ModelResponse


@pytest.mark.asyncio
async def test_dummy_provider_get_response():
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

    assert isinstance(resp, ModelResponse)
    assert resp.response_id == "local-1"
    assert len(resp.output) == 1
