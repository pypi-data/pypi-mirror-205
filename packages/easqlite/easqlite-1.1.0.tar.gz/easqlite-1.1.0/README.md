# easqlite
A simple Executor-based async sqlite wrapper.

This is used very similarly to the standard `sqlite3` module.

By default, `ThreadPoolExecutor(max_workers=1)` is used as the executor.  If you
pass your own executor, you are responsible for shutting it down and ensuring it
only uses one thread.

Differences from `sqlite3`:

* `connect` is not a function, but just an alias to the `Connection` class.
* `Connect` `check_same_thread` defaults to `__debug__` instead of `True`
* `Connection`'s constructor takes an optional `executor` argument.
* Every method, function, context manager, property accessor, and iterator is
  awaitable.
  * `Connection.interrupt` operates immediately without being `awaited`, and its
    returned coroutine is actually a no-op.
* Every call that takes a factory uses the factory for the internal calls, and
  defers to a statically defined wrapper class.  The internal calls will still
  use the factories.
* All objects with a `close` method are async context managers.
* All properties are now methods with an optional setter parameter, so they
  are properly awaitable and set and get on the same thread.
  * An exception to this is `Cursor.connection`, which is still a property.
* `Blob.__getitem__` is async, but `Blob.__setitem__` can not be.  `Blob.set` is
  provided instead, with the exact same semantics (it can be passed a `slice`).
  You can use `Blob.__setitem__`, but it doesn't actually directly set the blob,
  but rather queues a set to be run on flush.  Any other coroutine flushes the
  blob, or you can use an explicit `Blob.flush`, or just let the blob exit its
  context manager.
* `Blob.__len__` and `Blob.__bool__` block on the executor. `Blob.len` and
  `blob.bool` are async replacements for these.

`Connection`, `Cursor`, and `Blob` are lazy.  They will not open on
construction, but will open when awaited, or when entered as an asynchronous
context manager.

All these objects must be either awaited or used as an asynchronous context manager:

```python
# OK: The cursor was awaited
cursor = await connection.cursor()
await cursor.execute(sql)
async for row in cursor:
  do_something_with(row)

# ERROR: the cursor is not opened
cursor = connection.cursor()
await cursor.execute(sql)
async for row in cursor:
  do_something_with(row)

# OK: The cursor was entered (the preferred style)
async with connection.cursor() as cursor:
  await cursor.execute(sql)
  async for row in cursor:
    do_something_with(row)

# The connection.execute family are coroutines, and must be awaited.

# OK: The coroutine was awaited, and returns an open cursor.
async with await connection.execute(sql) as cursor:
  async for row in cursor:
    do_something_with(row)

# ERROR: The connection.execute result is a coroutine.  It is not a context manager
async with connection.execute(sql) as cursor:
  async for row in cursor:
    do_something_with(row)

# OK: connection.execute opens its cursor, it can just be iterated.
async for row in await connection.execute(sql):
  do_something_with(row)

# ERROR: __aiter__ is not defined on a running coroutine.  It must be awaited.
async for row in connection.execute(sql):
  do_something_with(row)
```

This can be used nearly identically to the regular sqlite module if you sprinkle
an `await` on every function call, but it is preferred to use the async context
managers everywhere possible.  You can't easily go wrong when using the context
managers.

Constants are not re-exported, so this library should usually be used in
conjunction with the core sqlite3 library.

This is very similar in spirit to the
[aiosqlite](https://github.com/omnilib/aiosqlite) project, but this one takes a
more earnest attempt at deferring responsibility to other components.  This one
also should be more responsive on close, because it doesn't rely on a timeout to
shut itself off.

This one also pushes much more extremely on async use, and defers everything it
can to the executor thread, even properties.

If you want a more mature and battle-tested package, use `aiosqlite`.  In my
rough tests, it performs better than this package as well.
