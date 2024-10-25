import requests
import json
import os
import hashlib
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date
import ciso8601
import pytz


from typing import Any, Dict
from cache import APIReqestCache

API_KEY = os.getenv("POLYGON_API_KEY")
CACHE = "api_response_cache"

def main() -> None:
    cache = APIReqestCache(cache_dir=CACHE)

    ticker = "AAPL"
    multiplier = 5
    timespan = "minute"
    start, end = market_open_close(2024, 10, 20)
    print(f"{start=}")
    print(f"{end=}")


    aggregates_query(cache, ticker, timespan, multiplier, start, end)

def market_open_close(year : int, month : int, day : int):
    """Takes a particular day and outputs market open and close times as Unix timestamps"""

    date = datetime(year, month, day)
    timezone = pytz.timezone('America/New_York')
    eastern_dt = timezone.localize(date)

    market_open = eastern_dt.replace(hour=9, minute=30)
    market_close = eastern_dt.replace(hour=16, minute=0)

    return int(market_open.timestamp() * 1000), int(market_close.timestamp() * 1000)


def aggregates_query(cache : APIReqestCache, ticker : str, timespan : str, multiplier : int, start : float, end : float) -> dict:
    timespan_options = set(['second', 'minute', 'hour', 'day', 'week', 'month', 'quater', 'quater', 'year'])

    if timespan not in timespan_options:
        raise ValueError(f"{__name__}() - {timespan} is not a valid option for timespan")
    
    url = f"""https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start}/{end}?adjusted=true&sort=asc&apiKey={API_KEY}"""

    res = cache.make_query(url)

    time_series_data = res['results']
    
    time_series_data_np  = np.array([[row[key] for key in row] for row in time_series_data])

    print(time_series_data[0].keys())
    np.set_printoptions(precision=3, suppress=True, linewidth=100)
    print(time_series_data_np)

    to_column = {}
    for column, key in enumerate(list(time_series_data[0].keys())):
        to_column[key] = column

    x = time_series_data_np[:, to_column['t']]

    print(f"start: {datetime.fromtimestamp(x[0] / 1000)} UTC")
    print(f"end: {datetime.fromtimestamp(x[-1] / 1000)} UTC")

    print(time_series_data_np.shape)

    fig, axs = plt.subplots(nrows=1, ncols=3)
    axs[0].plot(x, time_series_data_np[:, to_column['l']])
    axs[1].plot(x, time_series_data_np[:, to_column['h']])
    axs[2].plot(x, time_series_data_np[:, to_column['v']])
    
    plt.show()

if __name__ == "__main__":
    main()