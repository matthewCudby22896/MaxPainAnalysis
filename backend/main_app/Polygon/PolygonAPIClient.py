import os
import requests
from typing import Dict, Any, Optional, Tuple

API_KEY = os.getenv("POLYGON_API_KEY")

class PolygonAPIClient:
    """
    The sole purpose of the component is query the polygon API, and return the response in the expected format.
    """
    def __init__(self):
        self.api_key = API_KEY

        # TODO: Implement caching system (Django has it's own implementation)

    def fetch_ticker_details(self, ticker : str) -> Tuple[]:
        url = f"https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={self.api_key}"

        json : Optional[Dict[Any, Any]] = None

        try:
            res = requests.get(url)
            res.raise_for_status()
            json = res.json()

        except Exception as e:
            print("Failed to fetch ticker details: {e}")
            return None
        
        return json

        


