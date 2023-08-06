from collections.abc import Callable
import sqlite3

from typing import Any, Literal, TypeVar
from ._connection import Connection
from ._util import _exec

connect = Connection 

async def complete_statement(statement: str) -> bool:
    return await _exec(sqlite3.complete_statement, statement)

async def enable_callback_tracebacks(flag: bool,) -> None:
    return await _exec(sqlite3.enable_callback_tracebacks, flag)

AdapterType = TypeVar('AdapterType')

async def register_adapter(
    type: type[AdapterType],
    adapter: Callable[[AdapterType], None | int | float | str | bytes],
) -> None:
    return await _exec(sqlite3.register_adapter, type, adapter)

async def register_converter(
    typename: Literal['NULL', 'INTEGER', 'REAL', 'TEXT', 'BLOB'],
    converter: Callable[[bytes], Any]
) -> None:
    return await _exec(sqlite3.register_converter, typename, converter)

PARSE_COLNAMES = sqlite3.PARSE_COLNAMES
PARSE_DECLTYPES = sqlite3.PARSE_DECLTYPES
SQLITE_OK = sqlite3.SQLITE_OK
SQLITE_DENY = sqlite3.SQLITE_DENY
SQLITE_IGNORE = sqlite3.SQLITE_IGNORE
apilevel = sqlite3.apilevel
paramstyle = sqlite3.paramstyle
sqlite_version = sqlite3.sqlite_version
sqlite_version_info = sqlite3.sqlite_version_info
threadsafety = sqlite3.threadsafety
version = sqlite3.version
version_info = sqlite3.version_info

Row = sqlite3.Row
sqlite3.PrepareProtocol = sqlite3.PrepareProtocol

Warning = sqlite3.Warning
Error = sqlite3.Error
InterfaceError = sqlite3.InterfaceError
DatabaseError = sqlite3.DatabaseError
DataError = sqlite3.DataError
OperationalError = sqlite3.OperationalError
IntegrityError = sqlite3.IntegrityError
InternalError = sqlite3.InternalError
ProgrammingError = sqlite3.ProgrammingError
NotSupportedError = sqlite3.NotSupportedError
