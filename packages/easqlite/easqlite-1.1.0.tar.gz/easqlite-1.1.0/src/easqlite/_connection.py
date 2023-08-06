from os import PathLike
import sqlite3

from functools import partial
from concurrent.futures import Executor, ThreadPoolExecutor
from types import TracebackType
from typing import (
    Any, AsyncIterable, Awaitable, Generator, Iterable, Optional, Type, Union,
    overload, Callable,
)
from weakref import finalize
from asyncio import get_running_loop, Lock
from sys import version_info
from . import _blob, _cursor
from ._util import _Unset, _unset, _IterDump, _close_in_executor, _noop_awaitable
from ._types import ExecReturn, IsolationLevel, RowFactory, TextFactory

class Connection:
    __slots__ = (
        '__cached_statements',
        '__check_same_thread',
        '_connection',
        '__database',
        '__detect_types',
        '__dict__',
        '__executor_arg',
        '_executor',
        '__factory',
        '__finalizer',
        '__isolation_level',
        '__lock',
        '__opened',
        '__timeout',
        '__uri',
        '__weakref__',
    )
    def __init__(
        self,
        database: Union[str, bytes, PathLike],
        timeout: float = 5.0,
        detect_types: int = 0,
        isolation_level: Optional[IsolationLevel] = 'DEFERRED',
        check_same_thread: bool = __debug__,
        factory: Type[sqlite3.Connection] = sqlite3.Connection,
        cached_statements: int = 128,
        uri: bool = False,
        executor: Optional[Executor] = None,
    ) -> None:
        self.__database = database
        self.__timeout = timeout
        self.__detect_types = detect_types
        self.__isolation_level = isolation_level
        self.__check_same_thread = check_same_thread
        self.__factory = factory
        self.__cached_statements = cached_statements
        self.__uri = uri
        self.__executor_arg = executor

        self.__opened = False

        # Lock for opening and closing.
        self.__lock = Lock()

    async def _exec(
        self,
        function: Callable[..., ExecReturn],
        *args: Any,
        **kwargs: Any,
    ) -> ExecReturn:
        return await get_running_loop().run_in_executor(
            self._executor,
            partial(function, *args, **kwargs),
        )

    async def __open(self) -> None:
        '''Open the connection if it's not opened.
        '''
        async with self.__lock:
            if not self.__opened:
                if self.__executor_arg is None:
                    self._executor = ThreadPoolExecutor(max_workers=1)
                else:
                    self._executor = self.__executor_arg

                self._connection = await self._exec(
                    sqlite3.connect,
                    database = self.__database,
                    timeout = self.__timeout,
                    detect_types = self.__detect_types,
                    isolation_level = self.__isolation_level,
                    check_same_thread = self.__check_same_thread,
                    factory = self.__factory,
                    cached_statements = self.__cached_statements,
                    uri = self.__uri,
                )

                self.__finalizer = finalize(
                    self,
                    _close_in_executor,
                    self._executor,
                    self._connection,
                )

                self.__opened = True

    def __await__(self) -> Generator[None, None, 'Connection']:
        yield from self.__open().__await__()
        return self

    async def __aenter__(self) -> 'Connection':
        return await self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        try:
            if exc is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self.close()

    def cursor(
        self,
        factory: Type[sqlite3.Cursor] = sqlite3.Cursor,
    ) -> '_cursor.Cursor':
        return _cursor.Cursor(self, factory)

    if version_info >= (3, 11):
        def blobopen(
            self,
            table: str,
            column: str,
            row: str,
            *,
            readonly: bool = False,
            name: str = 'main',
        ) -> '_blob.Blob':
            return _blob.Blob(
                self,
                table=table,
                column=column,
                row=row,
                readonly=readonly,
                name=name,
            )

    async def commit(self) -> None:
        await self._exec(self._connection.commit)

    async def close(self) -> None:
        async with self.__lock:
            if self.__opened:
                try:
                    self.__opened = False
                    self.__finalizer.detach()
                    await self._exec(self._connection.close)
                    if self.__executor_arg is None:
                        self._executor.shutdown()
                finally:
                    del self.__finalizer, self._executor, self._connection

    async def rollback(self) -> None:
        await self._exec(self._connection.rollback)

    async def execute(
        self,
        sql: str,
        parameters: Iterable[Any] = (),
    ) -> '_cursor.Cursor':
        return await (await self.cursor()).execute(sql, parameters)

    async def executemany(
        self,
        sql: str,
        parameters: Iterable[Any],
    ) -> '_cursor.Cursor':
        return await (await self.cursor()).executemany(sql, parameters)

    async def executescript(self, sql_script: str) -> '_cursor.Cursor':
        return await (await self.cursor()).executescript(sql_script)

    if version_info >= (3, 8):
        async def create_function( # type: ignore
            self,
            name: str,
            narg: int,
            func: Callable[..., Optional[Any]],
            *,
            deterministic: bool = False,
        ) -> None:
            await self._exec(
                self._connection.create_function,
                name,
                narg,
                func,
                deterministic=deterministic,
            )
    else:
        async def create_function(
            self,
            name: str,
            narg: int,
            func: Callable[..., Optional[Any]],
        ) -> None:
            await self._exec(
                self._connection.create_function,
                name,
                narg,
                func,
            )

    async def create_aggregate(
        self,
        name: str,
        n_arg: int,
        aggregate_class: Optional[type],
    ) -> None:
        await self._exec(
            self._connection.create_aggregate,
            name,
            n_arg,
            aggregate_class,
        )

    if version_info >= (3, 11):
        async def create_window_function(
            self,
            name: str,
            num_params: int,
            aggregate_class: Optional[type],
        ) -> None:
            await self._exec(
                self._connection.create_window_function,
                name,
                num_params,
                aggregate_class,
            )

    async def create_collation(
        self,
        name: str,
        callable: Callable[[str, str], Optional[int]],
    ) -> None:
        await self._exec(
            self._connection.create_collation,
            name,
            callable,
        )

    def interrupt(self) -> Awaitable[None]:
        self._connection.interrupt()
        return _noop_awaitable

    async def set_authorizer(
        self,
        authorizer_callback: Callable[[
            int,
            Optional[str],
            Optional[str],
            Optional[str],
            Optional[str],
        ], Optional[int]],
    ) -> None:
        await self._exec(
            self._connection.set_authorizer,
            authorizer_callback,
        )

    async def set_progress_handler(
        self,
        progress_handler: Callable[[], Optional[int]],
        n: int,
    ) -> None:
        await self._exec(
            self._connection.set_progress_handler,
            progress_handler,
            n,
        )
    async def set_trace_callback(
        self,
        trace_callback: Callable[[str], Optional[Any]],
    ) -> None:
        await self._exec(
            self._connection.set_trace_callback,
            trace_callback,
        )

    async def enable_load_extension(
        self,
        enabled: bool,
    ) -> None:
        await self._exec(
            self._connection.enable_load_extension,
            enabled,
        )

    async def load_extension(
        self,
        path: str,
    ) -> None:
        await self._exec(
            self._connection.load_extension,
            path,
        )

    def iterdump(
        self,
    ) -> AsyncIterable[str]:
        return _IterDump(self, self._connection.iterdump)

    async def backup(
        self,
        target: Union['Connection', sqlite3.Connection],
        *,
        pages: int = -1,
        progress: Optional[Callable[[int, int, int], Any]] = None,
        name: str = 'main',
        sleep: float = 0.250,
    ) -> None:
        await self._exec(
            self._connection.backup,
            target,
            pages=pages,
            progress=progress,
            name=name,
            sleep=sleep,
        )

    async def getlimit(self, category: int) -> int:
        return await self._exec(
            self._connection.getlimit,
            category,
        )
    async def setlimit(self, category: int, limit: int) -> int:
        return await self._exec(
            self._connection.setlimit,
            category,
            limit,
        )

    if version_info >= (3, 11):
        async def serialize(self, *, name: str = 'main') -> bytes:
            return await self._exec(
                self._connection.serialize,
                name=name,
            )

        async def deserialize(self, data: bytes, *, name: str = 'main') -> None:
            await self._exec(
                self._connection.deserialize,
                bytes,
                name=name,
            )

    
    async def in_transaction(self) -> bool:
        return await self._exec(getattr, self._connection, 'in_transaction')

    @overload
    async def isolation_level(self) -> Optional[IsolationLevel]:
        ...

    @overload
    async def isolation_level(self, value: Optional[IsolationLevel]) -> None:
        ...

    async def isolation_level(
        self,
        value: Optional[Union[IsolationLevel, _Unset]] = _unset,
    ) -> Optional[IsolationLevel]:
        if value is _unset:
            return await self._exec(getattr, self._connection, 'isolation_level')
        else:
            await self._exec(setattr, self._connection, 'isolation_level', value)

    @overload
    async def row_factory(self) -> Optional[RowFactory]:
        ...

    @overload
    async def row_factory(self, value: Optional[RowFactory]) -> None:
        ...
            
    async def row_factory(
        self,
        value: Optional[Union[RowFactory, _Unset]] = _unset,
    ) -> Optional[RowFactory]:
        if value is _unset:
            return await self._exec(getattr, self._connection, 'row_factory')
        else:
            await self._exec(setattr, self._connection, 'row_factory', value)

    @overload
    async def text_factory(self) -> TextFactory:
        ...

    @overload
    async def text_factory(self, value: TextFactory) -> None:
        ...
            
    async def text_factory(
        self,
        value: Union[TextFactory, _Unset] = _unset,
    ) -> Optional[TextFactory]:
        if value is _unset:
            return await self._exec(getattr, self._connection, 'text_factory')
        else:
            await self._exec(setattr, self._connection, 'text_factory', value)
            
    async def total_changes(self) -> int:
        return await self._exec(getattr, self._connection, 'total_changes')
