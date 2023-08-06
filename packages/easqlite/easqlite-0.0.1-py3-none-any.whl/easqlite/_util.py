from collections.abc import Callable

from functools import partial
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import Any, AsyncIterable, Iterator, AsyncIterator, cast
from asyncio import get_running_loop
from . import _connection
from ._types import ExecReturn

class _Unset:
    pass

_unset = _Unset()

def _close_in_executor(executor: Executor, closeable: Any):
    '''A blocking finalizer that runs in the given executor.

    This should ideally never be relied upon.
    '''
    executor.submit(closeable.close).result()

_executor = ThreadPoolExecutor(max_workers=1)

async def _exec(
    function: Callable[..., ExecReturn],
    *args: Any,
    **kwargs: Any,
) -> ExecReturn:
    return await get_running_loop().run_in_executor(
        _executor,
        partial(function, *args, **kwargs),
    )

class _IterDump(AsyncIterable[str]):
    __slots__ = (
        '__connection',
        '__iterdump',
    )

    def __init__(
        self,
        connection: '_connection.Connection',
        iterdump: Callable[[], Iterator[str]],
    ) -> None:
        self.__connection = connection
        self.__iterdump = iterdump

    async def __aiter__(self) -> AsyncIterator[str]:
        iterator = await self.__connection._exec(self.__iterdump)
        return _IterDumpIterator(self.__connection, iterator)

class _IterDumpIterator(AsyncIterable[str]):
    __slots__ = (
        '__connection',
        '__iterator',
    )

    def __init__(
        self,
        connection: '_connection.Connection',
        iterator: Iterator[str]
    ) -> None:
        self.__connection = connection
        self.__iterator

    async def __anext__(self) -> str:
        try:
            return await self.__connection._exec(
                cast(Callable[..., str], next),
                self.__iterator,
            )
        except StopIteration:
            raise StopAsyncIteration
