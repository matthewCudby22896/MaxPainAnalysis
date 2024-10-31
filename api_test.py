import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
from typing import Tuple
import pandas
import mplfinance as mpf

from typing import Any, Dict
from cache import APIReqestCache

API_KEY = os.getenv("POLYGON_API_KEY")
CACHE = "api_response_cache"
TIMESPANS =  set(['second', 'minute', 'hour', 'day', 'week', 'month', 'quater', 'quater', 'year'])

class MarketDataHandler:

    def __init__(self):
        self.cache = APIReqestCache(cache_dir=CACHE)

    def generate_candle_plot(self, ticker : str, timespan : str, multiplier : str, date : str):
        market_open, market_close = self.market_open_close(date)

        url = f"""https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{market_open}/{market_close}?adjusted=true&sort=asc&apiKey={API_KEY}"""

        response = self.cache.make_query(url)
        if response is None:
            raise Exception(f"{__name__}() - response is None'")

        if 'results' not in response.keys():
            raise Exception(f"{__name__}() - no 'results' attribute within response dict")
        
        pricing_data = self.extract_pricing_data(response)

        mpf.plot(pricing_data, type='candle', style='yahoo', volume=True, title="Price Chart")  
    

    def extract_pricing_data(self, response: dict):
        to_col = {}
        for col, key in enumerate(response['results'][0].keys()):
            to_col[key] = col

        # filter out unwanted data
        desired_keys = ["v", "o", "c", "h", "l", "t"]
        feature_labels = ["volume", "open", "close", "high", "low", "time"]

        pricing_data = np.array([[row[key] for key in desired_keys] for row in response['results']])
        pricing_data = pandas.DataFrame(pricing_data, columns=feature_labels)

        pricing_data['time'] = pandas.to_datetime(pricing_data['time'], unit='ms')
        pricing_data.set_index('time', inplace=True)

        return pricing_data


    def market_open_close(self, date_str : str) -> Tuple[int, int]:
        # convert string to datetime
        date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # timezone setup
        timezone = pytz.timezone('America/New_York')

        # define market open and close times in UTC
        market_open_dt = timezone.localize(date.replace(hour=9, minute=30))
        market_close_dt = timezone.localize(date.replace(hour=16, minute=0))

        # convert to timestamps in milliseconds
        market_open = int(market_open_dt.timestamp() * 1000)
        market_close = int(market_close_dt.timestamp() * 1000)
        
        return market_open, market_close
    
    def fetch_eod_options_oi_data(self, ticker : str, expiration_date : str, as_of:str, type : str, expired : bool = True, limit : int = 1000):
        url = f"""https://api.polygon.io/v3/options/contracts?underlying_ticker={ticker}&contract_type={type}&expiration_date={expiration_date}&as_of={as_of}&expired={expired}&limit={limit}&apiKey={API_KEY}"""
        
        self.cache.make_query(url)




def main() -> None:
    np.set_printoptions(precision=3, suppress=True, linewidth=100)

    ticker = "GOOG"
    multiplier = 5
    timespan = "minute"
    date_str = "2024-10-24"

    graph_builder = MarketDataHandler()
    graph_builder.generate_candle_plot(ticker, timespan, multiplier, date_str)

    ticker = "ASML"
    expiration_date = "2024-10-25"
    as_of = "2024-10-25"
    type = "call"

    graph_builder.fetch_eod_options_oi_data(ticker, expiration_date, as_of, type)


    

if __name__ == "__main__":
    main()