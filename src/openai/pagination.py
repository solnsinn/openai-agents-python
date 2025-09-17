from __future__ import annotations

from typing import Generic, Iterable, Iterator, AsyncIterator, TypeVar, List

T = TypeVar("T")


class SyncCursorPage(Generic[T]):
    """A tiny shim of openai.pagination.SyncCursorPage used for type hints.

    This minimal implementation provides iteration over an in-memory list of items.
    """

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self.items: List[T] = list(items or [])

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)


class AsyncCursorPage(Generic[T]):
    """A tiny shim of openai.pagination.AsyncCursorPage used for type hints.

    Implements an async iterator over an in-memory list of items.
    """

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self.items: List[T] = list(items or [])

    def __aiter__(self) -> AsyncIterator[T]:
        async def _gen() -> AsyncIterator[T]:
            for item in self.items:
                yield item

        return _gen()
