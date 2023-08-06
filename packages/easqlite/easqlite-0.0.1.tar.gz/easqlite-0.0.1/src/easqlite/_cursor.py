import sqlite3

from types import TracebackType
from typing import Any, Iterable, overload
from . import _connection
from ._util import _Unset, _unset
from ._types import RowFactory

class Cursor:
    __slots__ = (
        '__connection',
        '__cursor',
        '__weakref__',
        '__dict__',
    )

    def __init__(
        self,
        connection: '_connection.Connection',
        cursor: sqlite3.Cursor,
    ) -> None:
        self.__connection = connection
        self.__cursor = cursor

    async def __aenter__(self) -> 'Cursor':
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType,
    ) -> None:
        await self.close()

    async def execute(self, sql: str, parameters: Iterable[Any] = ()) -> 'Cursor':
        await self.__connection._exec(self.__cursor.execute, sql, parameters)
        return self

    async def executemany(self, sql: str, parameters: Iterable[Any]) -> 'Cursor':
        await self.__connection._exec(self.__cursor.executemany, sql, parameters)
        return self

    async def executescript(self, sql_script: str) -> 'Cursor':
        await self.__connection._exec(self.__cursor.executescript, sql_script)
        return self

    async def close(self) -> None:
        await self.__connection._exec(self.__cursor.close)

    async def fetchone(self) -> Any:
        return await self.__connection._exec(self.__cursor.fetchone)

    async def fetchmany(self, size: int | None = None) -> list[Any]:
        if size is None:
            return await self.__connection._exec(self.__cursor.fetchmany, size)
        else:
            return await self.__connection._exec(self.__cursor.fetchmany)

    async def fetchall(self) -> list[Any]:
        return await self.__connection._exec(self.__cursor.fetchall)

    async def setinputsizes(self, sizes: Any) -> None:
        await self.__connection._exec(self.__cursor.setinputsizes, sizes)

    async def setoutputsize(self, size: Any, column: Any = None) -> None:
        await self.__connection._exec(self.__cursor.setoutputsize, size, column)

    
    @overload
    async def arraysize(self) -> int:
        ...

    @overload
    async def arraysize(self, value: int) -> None:
        ...

    async def arraysize(self, value: int | _Unset = _unset) -> int | None:
        if value is _unset:
            return await self.__connection._exec(
                getattr,
                self.__cursor,
                'arraysize',
            )
        else:
            await self.__connection._exec(
                setattr,
                self.__cursor,
                'arraysize',
                value,
            )

    @property
    def connection(self) -> '_connection.Connection':
        return self.__connection

    async def description(
        self,
    ) -> tuple[tuple[str, None, None, None, None, None, None], ...] | Any:
        return await self.__connection._exec(
            getattr,
            self.__cursor,
            'description',
        )

    async def lastrowid(self) -> int | None:
        return await self.__connection._exec(
            getattr,
            self.__cursor,
            'lastrowid',
        )

    async def rowcount(self) -> int:
        return await self.__connection._exec(
            getattr,
            self.__cursor,
            'rowcount',
        )

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
            return await self.__connection._exec(
                getattr,
                self.__cursor,
                'row_factory',
        )
        else:
            await self.__connection._exec(
                setattr,
                self.__cursor,
                'row_factory',
                value,
        )

    async def __aiter__(self) -> 'Cursor':
        return self

    async def __anext__(self) -> Any:
        try:
            return await self.__connection._exec(
                next,
                self.__cursor,
            )
        except StopIteration:
            raise StopAsyncIteration
        
