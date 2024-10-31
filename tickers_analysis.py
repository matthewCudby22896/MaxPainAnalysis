import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
from typing import Tuple
import pandas
import mplfinance as mpf

from typing import Any, Dict, List

import requests
from cache import APIReqestCache


API_KEY = os.getenv("POLYGON_API_KEY")

class TickerAnalyser():
    def __init__(self):
        pass

    def fetch_all_common_stock_data(self)-> Tuple[List[Any], str]:
        limit = 100
        all_tickers = []
        initial_url = f"""https://api.polygon.io/v3/reference/tickers?type=CS&market=stocks&active=true&limit={limit}&sort=ticker&apiKey={API_KEY}"""
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

    def has_options(self, ticker : str) -> bool:
        base_url = "https://api.polygon.io/v3/reference/options/contracts"
        params = {
            "underlying_ticker" : ticker,
            "limit" : 1,
            "apiKey" : API_KEY
        }
        try:    
            res : requests.Response = requests.get(base_url, params)
            res.raise_for_status()
            res_json = res.json()

        except Exception as e:
            print(f"{__name__}() - {e}")
        

        return len(res_json['results']) > 0


def main():
    ticker_analyser = TickerAnalyser()
    
    data, err = ticker_analyser.fetch_all_common_stock_data()
    filtered_data = []

    for i, entry in enumerate(data):
        ticker = entry['ticker']
        has_options_contracts = ticker_analyser.has_options(ticker)
        if has_options_contracts:
            print(f"{ticker} has options")
            filtered_data.append(ticker)
        else:
            print(f"{ticker} does not have options")
    
    print(f"{len(filtered_data)=}")


if __name__ == "__main__":
    main()