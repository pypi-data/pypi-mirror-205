import sqlite3

from typing import Any, Literal, TypeVar, Callable

ExecReturn = TypeVar('ExecReturn')
IsolationLevel = Literal['DEFERRED', 'IMMEDIATE', 'EXCLUSIVE']
RowFactory = Callable[[sqlite3.Cursor, tuple], Any]
TextFactory = Callable[[str], Any]
