import sqlite3

from typing import Any, Literal, Optional, Type, TypeVar, Callable, Union
from ._connection import Connection
from ._util import _exec

connect = Connection 

async def complete_statement(statement: str) -> bool:
    return await _exec(sqlite3.complete_statement, statement)

async def enable_callback_tracebacks(flag: bool,) -> None:
    return await _exec(sqlite3.enable_callback_tracebacks, flag)

AdapterType = TypeVar('AdapterType')

async def register_adapter(
    type: Type[AdapterType],
    adapter: Callable[[AdapterType], Optional[Union[int, float, str, bytes]]],
) -> None:
    return await _exec(sqlite3.register_adapter, type, adapter)

async def register_converter(
    typename: Literal['NULL', 'INTEGER', 'REAL', 'TEXT', 'BLOB'],
    converter: Callable[[bytes], Any]
) -> None:
    return await _exec(sqlite3.register_converter, typename, converter)
