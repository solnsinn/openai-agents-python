"""Minimal `openai` package shim for local development and tests.
Provide a small surface compatible with imports used in the repo (AsyncOpenAI and types).
This is a development-time shim; install the official `openai` package for real usage.
"""
from .client import AsyncOpenAI
from . import types

try:
	import httpx

	DefaultAsyncHttpxClient = httpx.AsyncClient
except Exception:
	class DefaultAsyncHttpxClient:
		def __init__(self, *args, **kwargs):
			pass

# Small typing helpers expected by the codebase. These are lightweight stubs for local
# testing only. For production use, install the official openai package.
class Omit:
	"""Placeholder type used to represent Omit[T, K] in type annotations."""

	def __init__(self, *args, **kwargs):
		pass

# Sentinel value used by some OpenAI types


class NotGiven:
	"""Sentinel type used to represent a missing value so `isinstance(x, NotGiven)` works.

	Upstream code sometimes does `isinstance(value, NotGiven)`. Using a class plus an
	instance preserves both identity checks (`x is NOT_GIVEN`) and isinstance checks.
	"""


NOT_GIVEN = NotGiven()

# Minimal AsyncStream placeholder used in type annotations for streaming responses.
from typing import Generic, TypeVar, AsyncIterator

T = TypeVar("T")


class AsyncStream(Generic[T]):
	"""A minimal AsyncStream placeholder supporting async iteration."""

	async def __aiter__(self) -> AsyncIterator[T]:
		if False:
			yield None  # pragma: no cover
		return


# Upstream code references NotGiven/NOT_GIVEN synonyms.
# Export the class as `NotGiven` and the instance as `NOT_GIVEN` so code can do
# both `x is NOT_GIVEN` and `isinstance(x, NotGiven)`.
NotGiven = NotGiven


# Minimal APIStatusError used by upstream callers to catch HTTP/API errors.
class APIStatusError(Exception):
	pass


# Keep a compatibility AuthenticationError so third-party packages can subclass it
class AuthenticationError(APIStatusError):
	pass


# Other common OpenAI exception names used by third-party libraries
class NotFoundError(APIStatusError):
	pass


class RateLimitError(APIStatusError):
	pass


class APIError(APIStatusError):
	pass


# A few more specific errors expected by third-party libs
class BadRequestError(APIStatusError):
	pass


class PermissionError(APIStatusError):
	pass


class ServiceUnavailableError(APIStatusError):
	pass


class UnprocessableEntityError(APIStatusError):
	pass


class APITimeoutError(APIStatusError):
	pass


class ServiceError(APIStatusError):
	pass


class PermissionDeniedError(PermissionError):
	pass


class PermissionRevokedError(PermissionError):
	pass


class InternalServerError(ServiceError):
	pass


class APIConnectionError(APIStatusError):
	pass


class NetworkError(APIConnectionError):
	pass


class ServiceTimeoutError(APIConnectionError):
	pass


class APIResponseValidationError(APIStatusError):
	pass


class OpenAIError(APIStatusError):
	pass

__all__ = [
	"AsyncOpenAI",
	"AsyncAzureOpenAI",
	"AzureOpenAI",
	"OpenAI",
	"types",
	"Omit",
	"DefaultAsyncHttpxClient",
	"AsyncStream",
	"NOT_GIVEN",
	"NotGiven",
	"APIStatusError",
	"AuthenticationError",
]

# Provider-specific aliases expected by some importers
AsyncAzureOpenAI = AsyncOpenAI
AzureOpenAI = AsyncOpenAI
OpenAI = AsyncOpenAI
