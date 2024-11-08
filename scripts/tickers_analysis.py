import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
from typing import Tuple
import pandas
import mplfinance as mpf
import json

from typing import Any, Dict, List

import requests
from cache import APIReqestCache


API_KEY = os.getenv("POLYGON_API_KEY")
CACHE_DIR = "./api_response_cache"
ALL_TICKERS_OUTPUT = "tickers_with_option_chains.json"

class TickerAnalyser():
    def __init__(self):
        self.cache = APIReqestCache(CACHE_DIR)

    def fetch_all_common_stock_data(self)-> Tuple[List[Any], str]:
        limit = 1000 # max of 1000
        all_tickers = []
        initial_url = f"""https://api.polygon.io/v3/reference/tickers?type=CS&market=stocks&active=true&limit={limit}&sort=ticker&apiKey={API_KEY}&market=XNYS"""
        url = initial_url

        i = 0
        while url:
            print(f"{i}")
            try:
                res : requests.Response = requests.get(url)
                res.raise_for_status()
                res_json : dict = res.json()

                all_tickers = res_json["results"] + all_tickers
                url = res_json.get("next_url", None)
                url = url + f"&apiKey={API_KEY}" if url else None


            except Exception as e:
                print(f"{__name__}() - {e}")
                return [], "warning - failed to fetch all common stock data!"

            i += 1
            
        return all_tickers, "success"
    
    def construct_url(self, base_url: str, params: dict) -> str:
        url = f"{base_url}?"
        for key, val in params.items():
            url += f"{key}={val}&"
            
        return url.rstrip('&')  # Remove the trailing '&'

    def has_options(self, ticker : str) -> bool:
        base_url = "https://api.polygon.io/v3/reference/options/contracts"
        params = {
            "underlying_ticker" : ticker,
            "limit" : 1,
            "apiKey" : API_KEY
        }
        
        url = self.construct_url(base_url, params)

        res, err = self.cache.make_query(url)
        if err:
            raise RuntimeError(err)
    
        return len(res['results']) > 0

def main():
    ticker_analyser = TickerAnalyser()
    
    data, err = ticker_analyser.fetch_all_common_stock_data()

    tickers_with_option_chains = []
    tickers_without_options_chains = []

    for i, entry in enumerate(data):
        ticker = entry['ticker']
        has_options_contracts = ticker_analyser.has_options(ticker)
        if has_options_contracts:
            print(f"{ticker} has options")
            tickers_with_option_chains.append(ticker)
        else:
            print(f"{ticker} does not have options")
            tickers_without_options_chains.append(ticker)
    
    to_save = {"tickers_with_option_chains" : tickers_with_option_chains, "tickers_without_options_chains" : tickers_without_options_chains}

    with open(ALL_TICKERS_OUTPUT, 'w') as f:
        json.dump(to_save, f)

    num_tickers_with_options = len(tickers_with_option_chains)
    num_tickers_without_options = len(tickers_without_options_chains)

    print(f"{num_tickers_with_options=}")
    print(f"{num_tickers_without_options}")


if __name__ == "__main__":
    main()