"""Package shim for openai.types.realtime submodules used by tests.

Expose commonly imported names as attributes to match the real SDK layout.
"""
from .realtime_audio_formats import (
    AudioPCM,
    AudioPCMA,
    AudioPCMU,
    RealtimeAudioFormats,
)

from .realtime_audio_config import RealtimeAudioConfig
from .realtime_session_create_request import RealtimeSessionCreateRequest
from .realtime_transcription_session_create_request import RealtimeTranscriptionSessionCreateRequest
from .realtime_tracing_config import TracingConfiguration as RealtimeTracingConfig

__all__ = [
    "AudioPCM",
    "AudioPCMA",
    "AudioPCMU",
    "RealtimeAudioFormats",
    "RealtimeAudioConfig",
    "RealtimeSessionCreateRequest",
    "RealtimeTranscriptionSessionCreateRequest",
    "RealtimeTracingConfig",
]
