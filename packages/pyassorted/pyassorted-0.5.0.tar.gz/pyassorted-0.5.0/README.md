# pyassorted #

A library has assorted utils in Pure-Python. There are 3 principles:

1. Light-weight
2. No dependencies
3. Pythonic usage.


* Documentation: https://dockhardman.github.io/pyassorted/
* PYPI: https://pypi.org/project/pyassorted/

## Installation ##
```shell
pip install pyassorted
```

## Modules ##
- pyassorted.asyncio.executor
- pyassorted.asyncio.utils
- pyassorted.cache.cache
- pyassorted.lock.filelock


## Examples ##

### pyassorted.asyncio ###

```python
import asyncio
from pyassorted.asyncio import run_func

def normal_func() -> bool:
    return True

async def async_func() -> bool:
    await asyncio.sleep(0.0)
    return True

async main():
    assert await run_func(normal_func) is True
    assert await run_func(async_func) is True

asyncio.run(main())
```

### pyassorted.cache ###

```python
import asyncio
from pyassorted.cache import LRU, cached

lru_cache = LRU()

# Cache function
@cached(lru_cache)
def add(a: int, b: int) -> int:
    return a + b

assert add(1, 2) == 3
assert lru_cache.hits == 0
assert lru_cache.misses == 1

assert add(1, 2) == 3
assert lru_cache.hits == 1
assert lru_cache.misses == 1

# Cache coroutine
@cached(lru_cache)
async def async_add(a: int, b: int) -> int:
    await asyncio.sleep(0)
    return a + b

assert add(1, 2) == 3
assert lru_cache.hits == 2
assert lru_cache.misses == 1
```

### pyassorted.lock ###

```python
from concurrent.futures import ThreadPoolExecutor
from pyassorted.lock import FileLock

number = 0
tasks_num = 100
lock = FileLock()

def add_one():
    global number
    with lock:
        number += 1

with ThreadPoolExecutor(max_workers=40) as executor:
    futures = [executor.submit(add_one) for _ in range(tasks_num)]
    for future in futures:
        future.result()

assert number == tasks_num
```
