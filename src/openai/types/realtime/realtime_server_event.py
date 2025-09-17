from __future__ import annotations

from typing import Any, Dict, Literal, Optional, Type, Annotated, Union

try:
    from pydantic import BaseModel

    # Define minimal event models used by the agent/tests with strict `type` discriminators.
    class ResponseOutputAudioDeltaEvent(BaseModel):
        type: Literal["response.output_audio.delta"]
        response_id: str
        item_id: str
        content_index: int
        delta: str
        # Optional extras commonly present
        output_index: Optional[int] = None
        event_id: Optional[str] = None

    class ResponseOutputAudioDoneEvent(BaseModel):
        type: Literal["response.output_audio.done"]
        item_id: str
        content_index: int
        # Optional extras
        response_id: Optional[str] = None
        event_id: Optional[str] = None

    class InputAudioBufferSpeechStartedEvent(BaseModel):
        type: Literal["input_audio_buffer.speech_started"]
        item_id: str
        audio_start_ms: int
        audio_end_ms: int
        event_id: Optional[str] = None

    class ResponseOutputAudioTranscriptDeltaEvent(BaseModel):
        type: Literal["response.output_audio_transcript.delta"]
        item_id: str
        response_id: str
        content_index: int
        delta: str
        event_id: Optional[str] = None

    class InputAudioBufferTimeoutTriggeredEvent(BaseModel):
        type: Literal["input_audio_buffer.timeout_triggered"]
        item_id: str
        audio_start_ms: int
        audio_end_ms: int
        event_id: Optional[str] = None

    class SessionCreatedEvent(BaseModel):
        type: Literal["session.created"]
        session: Dict[str, Any]

    class SessionUpdatedEvent(BaseModel):
        type: Literal["session.updated"]
        session: Dict[str, Any]

    class ErrorEvent(BaseModel):
        type: Literal["error"]
        error: Dict[str, Any]

    class ConversationItemDeletedEvent(BaseModel):
        type: Literal["conversation.item.deleted"]
        item_id: str

    class ConversationItemCreatedEvent(BaseModel):
        type: Literal["conversation.item.created"]
        item: Dict[str, Any]
        previous_item_id: Optional[str] = None

    class ConversationItemAddedEvent(BaseModel):
        type: Literal["conversation.item.added"]
        item: Dict[str, Any]

    class ConversationItemRetrievedEvent(BaseModel):
        type: Literal["conversation.item.retrieved"]
        item: Dict[str, Any]

    class ConversationItemInputAudioTranscriptionCompletedEvent(BaseModel):
        type: Literal["conversation.item.input_audio_transcription.completed"]
        item_id: str
        transcript: str

    class ConversationItemTruncatedEvent(BaseModel):
        type: Literal["conversation.item.truncated"]
        # Some payloads may include item id or audio ms; keep optional to be permissive
        item_id: Optional[str] = None
        audio_end_ms: Optional[int] = None

    class ResponseCreatedEvent(BaseModel):
        type: Literal["response.created"]

    class ResponseDoneEvent(BaseModel):
        type: Literal["response.done"]

    class ResponseOutputItemAddedEvent(BaseModel):
        type: Literal["response.output_item.added"]
        item: Dict[str, Any]

    class ResponseOutputItemDoneEvent(BaseModel):
        type: Literal["response.output_item.done"]
        item: Dict[str, Any]

    # Expose a wrapper class that behaves like a tagged union to pydantic
    # by implementing __get_pydantic_core_schema__.
    class RealtimeServerEvent:
        _choices: tuple[Type[BaseModel], ...] = (
            ResponseOutputAudioDeltaEvent,
            ResponseOutputAudioDoneEvent,
            InputAudioBufferSpeechStartedEvent,
            ResponseOutputAudioTranscriptDeltaEvent,
            InputAudioBufferTimeoutTriggeredEvent,
            SessionCreatedEvent,
            SessionUpdatedEvent,
            ErrorEvent,
            ConversationItemDeletedEvent,
            ConversationItemCreatedEvent,
            ConversationItemAddedEvent,
            ConversationItemRetrievedEvent,
            ConversationItemInputAudioTranscriptionCompletedEvent,
            ConversationItemTruncatedEvent,
            ResponseCreatedEvent,
            ResponseDoneEvent,
            ResponseOutputItemAddedEvent,
            ResponseOutputItemDoneEvent,
        )

        @classmethod
        def __get_pydantic_core_schema__(cls, _source, _handler):  # type: ignore[override]
            # Build a discriminated union schema on `type` for the choices
            from pydantic import TypeAdapter
            from pydantic import Field as _F
            from typing import Union as _Union

            adapter = TypeAdapter(Annotated[_Union[cls._choices], _F(discriminator="type")])  # type: ignore[name-defined]
            return adapter.core_schema  # type: ignore[attr-defined]

except Exception:
    # Fallback extremely-permissive class if pydantic isn't available
    class RealtimeServerEvent:  # type: ignore[no-redef]
        def __init__(self, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)


__all__ = ["RealtimeServerEvent"]
