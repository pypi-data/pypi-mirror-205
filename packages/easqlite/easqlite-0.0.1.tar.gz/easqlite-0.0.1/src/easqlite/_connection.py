from collections.abc import Callable
from os import PathLike
import sqlite3

from functools import partial
from concurrent.futures import ThreadPoolExecutor
from types import TracebackType
from typing import Any, AsyncIterable, Iterable, Union, overload
from weakref import finalize
from asyncio import get_running_loop
from sys import version_info
from . import _blob, _cursor
from ._util import _Unset, _unset, _IterDump
from ._types import ExecReturn, IsolationLevel, RowFactory, TextFactory


class Connection:
    __slots__ = (
        '__cached_statements',
        '__check_same_thread',
        '__connection',
        '__database',
        '__detect_types',
        '__dict__',
        '__executor',
        '__factory',
        '__finalizer',
        '__isolation_level',
        '__opened',
        '__timeout',
        '__uri',
        '__weakref__',
    )
    def __init__(
        self,
        database: str | bytes | PathLike,
        timeout: float = 5.0,
        detect_types: int = 0,
        isolation_level: IsolationLevel | None = 'DEFERRED',
        check_same_thread: bool = __debug__,
        factory: type[sqlite3.Connection] = sqlite3.Connection,
        cached_statements: int = 128,
        uri: bool = False,
    ) -> None:
        self.__database =  database
        self.__timeout =  timeout
        self.__detect_types =  detect_types
        self.__isolation_level =  isolation_level
        self.__check_same_thread =  check_same_thread
        self.__factory =  factory
        self.__cached_statements =  cached_statements
        self.__uri =  uri

        self.__opened = False

    async def _exec(
        self,
        function: Callable[..., ExecReturn],
        *args: Any,
        **kwargs: Any,
    ) -> ExecReturn:
        return await get_running_loop().run_in_executor(
            self.__executor,
            partial(function, *args, **kwargs),
        )

    async def __open(self) -> None:
        '''Open the connection if it's not opened.
        '''
        if not self.__opened:
            self.__executor = ThreadPoolExecutor(max_workers=1)
            self.__connection = await self._exec(
                sqlite3.connect,
                database = self.__database,
                timeout = self.__timeout,
                detect_types = self.__detect_types,
                isolation_level = self.__isolation_level,
                check_same_thread = self.__check_same_thread,
                factory = self.__factory,
                cached_statements = self.__cached_statements,
                uri = self.__uri,
                executor = self.__executor,
            )

            self.__finalizer: finalize

            self.__opened = True


    async def __aenter__(self) -> 'Connection':
        await self.__open()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType,
    ) -> None:
        try:
            if exc is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self.close()

    async def cursor(
        self,
        factory: type[sqlite3.Cursor] = sqlite3.Cursor,
    ) -> '_cursor.Cursor':
        await self.__open()

        return _cursor.Cursor(self, await self._exec(self.__connection.cursor, factory))

    if version_info >= (3, 11):
        async def blobopen(
            self,
            table: str,
            column: str,
            row: str,
            *,
            readonly: bool = False,
            name: str = 'main',
        ) -> '_blob.Blob':
            await self.__open()

            return _blob.Blob(
                self,
                await self._exec(self.__connection.blobopen,
                    table,
                    column,
                    row,
                    readonly=readonly,
                    name=name,
                ),
            )

    async def commit(self) -> None:
        await self._exec(self.__connection.commit)

    async def close(self) -> None:
        if self.__opened:
            self.__finalizer.detach()
            await self._exec(self.__connection.close)
            self.__opened = False
            self.__executor.shutdown()

    async def rollback(self) -> None:
        await self._exec(self.__connection.rollback)

    async def execute(
        self,
        sql: str,
        parameters: Iterable[Any] = (),
    ) -> '_cursor.Cursor':
        cursor = await self.cursor()
        await cursor.execute(sql, parameters)
        return cursor

    async def executemany(
        self,
        sql: str,
        parameters: Iterable[Any],
    ) -> '_cursor.Cursor':
        cursor = await self.cursor()
        await cursor.executemany(sql, parameters)
        return cursor

    async def executescript(self, sql_script: str) -> '_cursor.Cursor':
        cursor = await self.cursor()
        await cursor.executescript(sql_script)
        return cursor

    if version_info >= (3, 8):
        async def create_function( # type: ignore
            self,
            name: str,
            narg: int,
            func: Callable[..., Any] | None,
            *,
            deterministic: bool = False,
        ) -> None:
            await self._exec(
                self.__connection.create_function,
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
            func: Callable[..., Any] | None,
        ) -> None:
            await self._exec(
                self.__connection.create_function,
                name,
                narg,
                func,
            )

    async def create_aggregate(
        self,
        name: str,
        n_arg: int,
        aggregate_class: type | None,
    ) -> None:
        await self._exec(
            self.__connection.create_aggregate,
            name,
            n_arg,
            aggregate_class,
        )

    if version_info >= (3, 11):
        async def create_window_function(
            self,
            name: str,
            num_params: int,
            aggregate_class: type | None,
        ) -> None:
            await self._exec(
                self.__connection.create_window_function,
                name,
                num_params,
                aggregate_class,
            )

    async def create_collation(
        self,
        name: str,
        callable: Callable[[str, str], int] | None,
    ) -> None:
        await self._exec(
            self.__connection.create_collation,
            name,
            callable,
        )

    def interrupt(self) -> None:
        self.__connection.interrupt()

    async def set_authorizer(
        self,
        authorizer_callback: Callable[[
            int,
            str | None,
            str | None,
            str | None,
            str | None,
        ], int] | None,
    ) -> None:
        await self._exec(
            self.__connection.set_authorizer,
            authorizer_callback,
        )

    async def set_progress_handler(
        self,
        progress_handler: Callable[[], int | None] | None,
        n: int,
    ) -> None:
        await self._exec(
            self.__connection.set_progress_handler,
            progress_handler,
            n,
        )
    async def set_trace_callback(
        self,
        trace_callback: Callable[[str], Any] | None,
    ) -> None:
        await self._exec(
            self.__connection.set_trace_callback,
            trace_callback,
        )

    async def enable_load_extension(
        self,
        enabled: bool,
    ) -> None:
        await self._exec(
            self.__connection.enable_load_extension,
            enabled,
        )

    async def load_extension(
        self,
        path: str,
    ) -> None:
        await self._exec(
            self.__connection.load_extension,
            path,
        )

    def iterdump(
        self,
    ) -> AsyncIterable[str]:
        return _IterDump(self, self.__connection.iterdump)

    async def backup(
        self,
        target: Union['Connection', sqlite3.Connection],
        *,
        pages: int = -1,
        progress: Callable[[int, int, int], Any] | None = None,
        name: str = 'main',
        sleep: float = 0.250,
    ) -> None:
        await self._exec(
            self.__connection.backup,
            target,
            pages=pages,
            progress=progress,
            name=name,
            sleep=sleep,
        )

    async def getlimit(self, category: int) -> int:
        return await self._exec(
            self.__connection.getlimit,
            category,
        )
    async def setlimit(self, category: int, limit: int) -> int:
        return await self._exec(
            self.__connection.setlimit,
            category,
            limit,
        )

    if version_info >= (3, 11):
        async def serialize(self, *, name: str = 'main') -> bytes:
            return await self._exec(
                self.__connection.serialize,
                name=name,
            )

        async def deserialize(self, data: bytes, *, name: str = 'main') -> None:
            await self._exec(
                self.__connection.deserialize,
                bytes,
                name=name,
            )

    
    async def in_transaction(self) -> bool:
        return await self._exec(getattr, self.__connection, 'in_transaction')

    @overload
    async def isolation_level(self) -> IsolationLevel | None:
        ...

    @overload
    async def isolation_level(self, value: IsolationLevel | None) -> None:
        ...

    async def isolation_level(
        self,
        value: IsolationLevel | None | _Unset = _unset,
    ) -> IsolationLevel | None:
        if value is _unset:
            return await self._exec(getattr, self.__connection, 'isolation_level')
        else:
            await self._exec(setattr, self.__connection, 'isolation_level', value)

    @overload
    async def row_factory(self) -> RowFactory | None:
        ...

    @overload
    async def row_factory(self, value: None | RowFactory) -> None:
        ...
            
    async def row_factory(
        self,
        value: None | RowFactory | _Unset = _unset,
    ) -> RowFactory | None:
        if value is _unset:
            return await self._exec(getattr, self.__connection, 'row_factory')
        else:
            await self._exec(setattr, self.__connection, 'row_factory', value)

    @overload
    async def text_factory(self) -> TextFactory:
        ...

    @overload
    async def text_factory(self, value: TextFactory) -> None:
        ...
            
    async def text_factory(
        self,
        value: TextFactory | _Unset = _unset,
    ) -> TextFactory | None:
        if value is _unset:
            return await self._exec(getattr, self.__connection, 'text_factory')
        else:
            await self._exec(setattr, self.__connection, 'text_factory', value)
            
    async def total_changes(self) -> int:
        return await self._exec(getattr, self.__connection, 'total_changes')
