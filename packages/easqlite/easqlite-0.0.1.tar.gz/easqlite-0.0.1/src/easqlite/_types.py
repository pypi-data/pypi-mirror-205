from collections.abc import Callable
import sqlite3

from typing import Any, Literal, TypeVar

ExecReturn = TypeVar('ExecReturn')
IsolationLevel = Literal['DEFERRED', 'IMMEDIATE', 'EXCLUSIVE']
RowFactory = Callable[[sqlite3.Cursor, tuple], Any]
TextFactory = Callable[[str], Any]
