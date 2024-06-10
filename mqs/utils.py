"""Common utility functions."""

from typing import AsyncIterable, TypeVar

T = TypeVar("T")


async def alist(gen: AsyncIterable[T]) -> list[T]:
    """Return all items yielded from `gen`."""
    return [m async for m in gen]
