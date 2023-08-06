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

                async with connection.cursor() as cursor:
                    sql = 'SELECT id, alpha, beta FROM foo ORDER BY id ASC'
                    await cursor.execute(sql)
                    self.assertEqual(await cursor.fetchmany(), [(1, None, b'Beta test one')])
                    self.assertEqual(await cursor.fetchmany(), [(2, 'Alpha test two', b'Beta test two')])
                    self.assertEqual(await cursor.fetchmany(), [])

                async with connection.cursor() as cursor:
                    sql = 'SELECT id, alpha, beta FROM foo ORDER BY id ASC'
                    await cursor.execute(sql)
                    self.assertEqual(await cursor.fetchmany(1000), [
                        (1, None, b'Beta test one'),
                        (2, 'Alpha test two', b'Beta test two'),
                    ])

                async with connection.cursor() as cursor:
                    sql = 'SELECT id, alpha, beta FROM foo ORDER BY id ASC'
                    await cursor.execute(sql)
                    await cursor.arraysize(-1)
                    self.assertEqual(await cursor.fetchmany(), [
                        (1, None, b'Beta test one'),
                        (2, 'Alpha test two', b'Beta test two'),
                    ])

                async with connection.cursor() as cursor:
                    sql = 'SELECT id, alpha, beta FROM foo ORDER BY id ASC'
                    await cursor.execute(sql)
                    self.assertEqual(await cursor.fetchmany(-1), [
                        (1, None, b'Beta test one'),
                        (2, 'Alpha test two', b'Beta test two'),
                    ])

                async with connection.cursor() as cursor:
                    sql = 'SELECT id, alpha, beta FROM foo ORDER BY id ASC'
                    await cursor.execute(sql)
                    self.assertEqual(await cursor.fetchall(), [
                        (1, None, b'Beta test one'),
                        (2, 'Alpha test two', b'Beta test two'),
                    ])

                async with connection.cursor() as cursor:
                    sql = 'SELECT id, alpha, beta FROM foo ORDER BY id ASC'
                    rows = []
                    async for row in await cursor.execute(sql):
                        rows.append(row)

                    self.assertEqual(rows, [
                        (1, None, b'Beta test one'),
                        (2, 'Alpha test two', b'Beta test two'),
                    ])
