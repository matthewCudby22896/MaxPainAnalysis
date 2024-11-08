from PolygonAPIClient import PolygonAPIClient
from typing import Dict, Any

class PolygonService:
    def __init__(self):
        self.api_client = PolygonAPIClient()

    def get_ticker_details(self, ticker: str) -> Dict[str, Any]:
        # Call the API client to fetch ticker details
        res = self.api_client.fetch_ticker_details(ticker)

        if not res:
            return {
                "query_success": False,
                "ticker_found": False
            }

        if res.get("status") == "NOT_FOUND":
            return {
                "query_success": True,
                "ticker_found": False
            }

        if res.get("status") == "OK" and "results" in res:
            details = res["results"]
            return {
                "query_success": True,
                "ticker_found": True,
                "ticker": details.get("ticker"),
                "name": details.get("name"),
                "actively_traded": details.get("active"),
                "market_cap": details.get("market_cap")
            }

        # Case 4: Unknown response status - raise an error
        raise RuntimeError("Error - unknown response status")

