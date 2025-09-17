"""Lightweight shim for `openai` used in local tests and notebooks.
This provides an `AsyncOpenAI` placeholder and minimal objects referenced by the codebase.
Do not use this shim in production; instead install the real `openai` package and configure API keys.
"""
import asyncio
from typing import Any

class AsyncOpenAI:
    """A minimal stub for AsyncOpenAI used for local imports and tests."""
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    async def chat(self, *args, **kwargs) -> Any:
        # simple placeholder response
        await asyncio.sleep(0)
        return {"choices": [{"message": {"content": "(shim) no-op response"}}]}

# Provide a compat alias if code expects a sync client
OpenAI = AsyncOpenAI


# Minimal exception hierarchy expected by some downstream packages (litellm etc.)
class APIError(Exception):
    """Base API-related error."""


class AuthenticationError(APIError):
    """Authentication failure."""


__all__ = ["AsyncOpenAI", "OpenAI", "APIError", "AuthenticationError"]
