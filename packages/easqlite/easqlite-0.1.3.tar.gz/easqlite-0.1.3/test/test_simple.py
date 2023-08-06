import unittest
import sqlite3
import easqlite
import asyncio 
import tempfile
from pathlib import Path

class SimpleTests(unittest.IsolatedAsyncioTestCase):
    async def test_some_queries(self):
        with tempfile.TemporaryDirectory() as dir:
            db = Path(dir) / "test.db"
            async with easqlite.connect(Path(dir) / "test.db", isolation_level=None) as connection:
                await connection.execute('''
                    CREATE TABLE foo (
                        id INTEGER PRIMARY KEY NOT NULL,
                        alpha TEXT NULL,
                        beta BLOB NOT NULL
                    )
                ''')

                async with connection.cursor() as cursor:
                    sql = 'INSERT INTO foo (id, alpha, beta) VALUES (?, ?, ?)'
                    await cursor.execute(sql, (1, None, b'Beta test one'))
                    await cursor.execute(sql, (2, 'Alpha test two', b'Beta test two'))
                    await connection.commit()


                async with connection.cursor() as cursor:
                    sql = 'SELECT id, alpha, beta FROM foo ORDER BY id ASC'
                    await cursor.execute(sql)
                    self.assertEqual(await cursor.fetchone(), (1, None, b'Beta test one'))
                    self.assertEqual(await cursor.fetchone(), (2, 'Alpha test two', b'Beta test two'))
                    self.assertIs(await cursor.fetchone(), None)
