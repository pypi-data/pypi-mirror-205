import sqlite3

from types import TracebackType
from typing import Any, Iterable, List, Optional, Tuple, Type, Union, overload
from . import _connection
from ._util import _Unset, _unset
from ._types import RowFactory
from asyncio import Lock

class Cursor:
    __slots__ = (
        '__connection',
        '__factory',
        '__cursor',
        '__opened',
        '__lock',
        '__weakref__',
        '__dict__',
    )

    def __init__(
        self,
        connection: '_connection.Connection',
        factory: Type[sqlite3.Cursor] = sqlite3.Cursor,
    ) -> None:
        self.__connection = connection
        self.__factory = factory
        self.__opened = False

        # Lock for opening and closing.
        self.__lock = Lock()

    async def _open(self) -> None:
        async with self.__lock:
            if not self.__opened:
                await self.__connection._open()
                self.__cursor = await self.__connection._exec(
                    self.__connection._connection.cursor,
                    self.__factory,
                )
                self.__opened = True

    async def __aenter__(self) -> 'Cursor':
        await self._open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def execute(self, sql: str, parameters: Iterable[Any] = ()) -> 'Cursor':
        await self._open()
        await self.__connection._exec(self.__cursor.execute, sql, parameters)
        return self

    async def executemany(self, sql: str, parameters: Iterable[Any]) -> 'Cursor':
        await self._open()
        await self.__connection._exec(self.__cursor.executemany, sql, parameters)
        return self

    async def executescript(self, sql_script: str) -> 'Cursor':
        await self._open()
        await self.__connection._exec(self.__cursor.executescript, sql_script)
        return self

    async def close(self) -> None:
        async with self.__lock:
            if self.__opened:
                try:
                    await self.__connection._exec(self.__cursor.close)
                finally:
                    self.__opened = False

    async def fetchone(self) -> Any:
        await self._open()
        return await self.__connection._exec(self.__cursor.fetchone)

    async def fetchmany(self, size: Optional[int] = None) -> List[Any]:
        await self._open()
        if size is None:
            return await self.__connection._exec(self.__cursor.fetchmany, size)
        else:
            return await self.__connection._exec(self.__cursor.fetchmany)

    async def fetchall(self) -> List[Any]:
        await self._open()
        return await self.__connection._exec(self.__cursor.fetchall)

    async def setinputsizes(self, sizes: Any) -> None:
        await self._open()
        await self.__connection._exec(self.__cursor.setinputsizes, sizes)

    async def setoutputsize(self, size: Any, column: Any = None) -> None:
        await self._open()
        await self.__connection._exec(self.__cursor.setoutputsize, size, column)

    @overload
    async def arraysize(self) -> int:
        ...

    @overload
    async def arraysize(self, value: int) -> None:
        ...

    async def arraysize(self, value: Union[int, _Unset] = _unset) -> Optional[int]:
        await self._open()
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
    ) -> Optional[Tuple[Tuple[str, None, None, None, None, None, None], ...]]:
        await self._open()
        return await self.__connection._exec(
            getattr,
            self.__cursor,
            'description',
        )

    async def lastrowid(self) -> Optional[int]:
        await self._open()
        return await self.__connection._exec(
            getattr,
            self.__cursor,
            'lastrowid',
        )

    async def rowcount(self) -> int:
        await self._open()
        return await self.__connection._exec(
            getattr,
            self.__cursor,
            'rowcount',
        )

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
        await self._open()
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

    def __aiter__(self) -> 'Cursor':
        return self

    async def __anext__(self) -> Any:
        await self._open()
        try:
            return await self.__connection._exec(
                next,
                self.__cursor,
            )
        except StopIteration:
            raise StopAsyncIteration
        
