from __future__ import annotations

from collections.abc import AsyncIterator

from agents.models.interface import Model, ModelProvider
from agents.items import ModelResponse, TResponseStreamEvent


class DummyModel(Model):
    """Minimal in-process model for examples and tests.

    It returns a deterministic assistant message and an empty Usage object.
    """

    async def get_response(
        self,
        system_instructions,
        input,
        model_settings,
        tools,
        output_schema,
        handoffs,
        tracing,
        *,
        previous_response_id=None,
        conversation_id=None,
        prompt=None,
    ) -> ModelResponse:
        text = "I recommend writing small, focused tests that cover one behavior each."

        # Try to produce an actual ResponseOutputMessage instance from the OpenAI SDK
        # so the library's isinstance checks (e.g. in _run_impl.process_model_response)
        # recognize it as a message. Fall back to a dict if constructing the model fails
        # for any reason (keeps tests robust across environments).
        try:
            # Import the package-level symbols so the created objects match the
            # classes used by the rest of the library (isinstance checks will pass).
            from openai.types.responses import ResponseOutputText, ResponseOutputMessage

            content_item = ResponseOutputText(annotations=[], text=text, type="output_text")
            message = ResponseOutputMessage(
                id="local-msg-1",
                content=[content_item],
                role="assistant",
                status="completed",
                type="message",
            )
        except Exception:
            # Import or validation failed; fall back to dict-shaped message understood by
            # ItemHelpers and ModelResponse.to_input_items.
            message = {
                "id": "local-msg-1",
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{"text": text}],
            }

        # import Usage lazily to avoid import-time cycles in some test environments
        from agents.usage import Usage

        usage = Usage()
        return ModelResponse(output=[message], usage=usage, response_id="local-1")

    def stream_response(
        self,
        system_instructions,
        input,
        model_settings,
        tools,
        output_schema,
        handoffs,
        tracing,
        *,
        previous_response_id=None,
        conversation_id=None,
        prompt=None,
    ) -> AsyncIterator[TResponseStreamEvent]:
        async def _gen():
            # No-op async generator
            if False:
                yield  # type: ignore

        return _gen()


class DummyProvider(ModelProvider):
    def get_model(self, model_name: str | None) -> Model:
        return DummyModel()
