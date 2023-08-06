from sys import version_info
if version_info >= (3, 11):
    from collections import deque
    from typing import SupportsIndex, Optional, Type, Any, Generator
    from collections.abc import Coroutine
    from types import TracebackType
    from asyncio import Lock
    from . import _connection

    class Blob:
        __slots__ = (
            '__connection',
            '__blob',
            '__setitems',
            '__opened',
            '__lock',
            '__table',
            '__column',
            '__row',
            '__readonly',
            '__name',
            '__weakref__',
            '__dict__',
        )

        def __init__(
            self,
            connection: '_connection.Connection',
            table: str,
            column: str,
            row: str,
            *,
            readonly: bool = False,
            name: str = 'main',
        ) -> None:
            self.__connection = connection
            self.__table = table
            self.__column = column
            self.__row = row
            self.__readonly = readonly
            self.__name = name
            self.__setitems: deque[Coroutine[None, None, None]] = deque()

            # Lock for opening and closing.
            self.__lock = Lock()

        async def _open(self) -> None:
            async with self.__lock:
                if not self.__opened:
                    await self.__connection._open()
                    self.__blob = await self.__connection._exec(
                        self.__connection._connection.blobopen,
                        self.__table,
                        self.__column,
                        self.__row,
                        readonly=self.__readonly,
                        name=self.__name,
                    )
                    self.__opened = True

        def __await__(self) -> Generator[Any, Any, 'Blob']:
            yield from self._open().__await__()
            return self

        async def __aenter__(self) -> 'Blob':
            await self._open()
            return self

        async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc: Optional[BaseException],
            traceback: Optional[TracebackType],
        ) -> None:
            await self.close()

        async def close(self) -> None:
            async with self.__lock:
                if self.__opened:
                    try:
                        try:
                            await self.flush()
                        finally:
                            await self.__connection._exec(self.__blob.close)
                    finally:
                        self.__opened = False


        async def read(self, length: int = -1) -> bytes:
            await self.flush()
            return await self.__connection._exec(self.__blob.read, length)

        async def write(self, data: bytes) -> None:
            await self.flush()
            await self.__connection._exec(self.__blob.write, bytes)

        async def tell(self) -> int:
            await self.flush()
            return await self.__connection._exec(self.__blob.tell)

        async def seek(self, offset: int, origin: int = 0) -> None:
            await self.flush()
            await self.__connection._exec(self.__blob.seek, offset, origin)

        async def flush(self) -> None:
            await self._open()
            while self.__setitems:
                await self.__setitems.popleft()

        async def __getitiem__(self, index: SupportsIndex | slice) -> int | bytes:
            await self.flush()
            return await self.__connection._exec(self.__blob.__getitem__, index)

        async def set(self, index: SupportsIndex | slice, value: int | bytes) -> None:
            await self.flush()
            await self.__set(index, value)

        async def __set(self, index: SupportsIndex | slice, value: int | bytes) -> None:
            await self.__connection._exec(self.__blob.__setitem__, index, value)

        def __setitem__(self, index: SupportsIndex | slice, value: int | bytes) -> None:
            self.__setitems.append(self.__set(index, value))

        def __len__(self) -> int:
            return self.__connection._executor.submit(len, self.__blob).result(1)

        def __bool__(self) -> bool:
            return self.__connection._executor.submit(bool, self.__blob).result(1)

        async def len(self) -> int:
            await self.flush()
            return await self.__connection._exec(len, self.__blob)

        async def bool(self) -> bool:
            await self.flush()
            return await self.__connection._exec(bool, self.__blob)


