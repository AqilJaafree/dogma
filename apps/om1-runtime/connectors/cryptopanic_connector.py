"""
CryptoPanic API Connector

Connector for fetching cryptocurrency news from CryptoPanic API.
Free tier: 50 requests/hour
"""

import requests
from typing import Dict, List


class CryptoPanicConnector:
    """Connector for CryptoPanic API (crypto news sentiment)"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://cryptopanic.com/api/v1"

    def get_posts(self, currencies: str = 'BTC', kind: str = 'news', filter_type: str = 'hot') -> Dict:
        """Fetch recent crypto news posts"""
        # TODO: Implement
        pass
