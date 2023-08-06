from collections import deque
from sys import version_info
if version_info >= (3, 11):
    from typing import SupportsIndex
    from collections.abc import Coroutine
    from typing import NoReturn
    import sqlite3
    from types import TracebackType
    from . import _connection

    class Blob:
        __slots__ = (
            '__connection',
            '__blob',
            '__setitems',
            '__weakref__',
            '__dict__',
        )

        def __init__(
            self,
            connection: '_connection.Connection',
            blob: 'sqlite3.Blob',
        ) -> None:
            self.__connection = connection
            self.__blob = blob
            self.__setitems: deque[Coroutine[None, None, None]] = deque()

        async def __aenter__(self) -> 'Blob':
            return self

        async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            traceback: TracebackType,
        ) -> None:
            await self.close()

        async def close(self) -> None:
            try:
                await self.flush()
            finally:
                await self.__connection._exec(self.__blob.close)

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

        def __len__(self) -> NoReturn:
            raise NotImplementedError('Use the len method instead')

        def __bool__(self) -> NoReturn:
            raise NotImplementedError('Use the bool method instead')

        async def len(self) -> int:
            await self.flush()
            return await self.__connection._exec(len, self.__blob)

        async def bool(self) -> bool:
            await self.flush()
            return await self.__connection._exec(bool, self.__blob)


