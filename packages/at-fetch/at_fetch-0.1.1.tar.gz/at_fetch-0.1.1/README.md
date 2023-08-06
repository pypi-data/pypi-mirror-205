## at_fetch

```
pip install at_fetch
poetry add at_fetch
```

### example

```
poetry install
poetry run python -m example.start_time
```

### usage

```
from fetch.fetch import Fetch
import asyncio
import time


async def main():
    request = Fetch()
    start_time = 1502913600
    end_time = 1533687900
    symbol = "btcusdt"
    interval = "1m"
    start = time.time()
    # await asyncio.sleep(1)
    res = await request.get_all_klines_data(
        "http://47.243.179.153:8000/api/kline/spot", symbol, interval, start_time, end_time
    )
    end = time.time()
    exec_time = end - start
    print("res", len(res))
    print("exec_time", exec_time)


asyncio.run(main())

```