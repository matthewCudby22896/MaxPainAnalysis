from Polygon.PolygonService import PolygonService
import re

from typing import Tuple, Dict, Optional
from constants import Json

import logging

logger = logging.getLogger(__name__)

class MaxPainChartingService:
    def __init__(self):
        self.polygon_service = PolygonService()
    
    def get_ticker_details(self, ticker : str) -> Tuple[Optional[Json], Optional[str]]:
        # Validate the ticker format
        if not re.fullmatch(r'[A-Z]+', ticker):
            return None, "Error - invalid format for ticker"

        try:
            # Query the polygon service for details
            details = self.polygon_service.get_ticker_details(ticker)

        except Exception:
            # Log unexpected erros
            logger.error("Unexpected error when fetching ticker details: {e}")
            return None, "Error - unexpected internal server error"

        # Check if query was succesful
        if not details.get("query_success"):
            return None, "Error - polygon api query failed"
        
        # Return succesful response
        else:
            return details, None

