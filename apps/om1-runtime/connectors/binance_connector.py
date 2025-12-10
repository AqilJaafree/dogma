"""
Bitcoin Price Connector with Multiple Fallbacks

Supports multiple free APIs for Bitcoin price data:
1. Binance API (Primary) - Most reliable, real-time data
2. CoinGecko API (Backup) - Free tier, no key required
3. CoinCap API (Backup 2) - Free, no key required

No API keys required for any of these endpoints.
"""

import requests
import os
from typing import Dict, List, Optional
from datetime import datetime


class BitcoinPriceConnector:
    """
    Multi-source Bitcoin price connector with automatic fallback.

    Tries sources in order:
    1. Binance (fastest, most reliable)
    2. CoinGecko (good backup)
    3. CoinCap (simple backup)
    """

    def __init__(self):
        self.binance_url = os.getenv('BINANCE_API_URL', 'https://api.binance.com/api/v3')
        self.coingecko_url = os.getenv('COINGECKO_API_URL', 'https://api.coingecko.com/api/v3')
        self.coincap_url = os.getenv('COINCAP_API_URL', 'https://api.coincap.io/v2')

    def get_current_price(self) -> Dict:
        """
        Get current Bitcoin price with automatic fallback.

        Returns:
            Dict with price, source, and metadata

        Example:
            >>> connector = BitcoinPriceConnector()
            >>> data = connector.get_current_price()
            >>> print(f"BTC: ${data['price']:,.2f} from {data['source']}")
        """
        # Try Binance first
        try:
            return self._get_from_binance()
        except Exception as e:
            print(f"Binance failed: {e}, trying CoinGecko...")

        # Fallback to CoinGecko
        try:
            return self._get_from_coingecko()
        except Exception as e:
            print(f"CoinGecko failed: {e}, trying CoinCap...")

        # Last resort: CoinCap
        try:
            return self._get_from_coincap()
        except Exception as e:
            print(f"All sources failed. Last error: {e}")
            raise Exception("All Bitcoin price sources unavailable")

    def _get_from_binance(self) -> Dict:
        """Get price from Binance API"""
        url = f"{self.binance_url}/ticker/24hr"
        response = requests.get(url, params={'symbol': 'BTCUSDT'}, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            'price': float(data['lastPrice']),
            'price_change_24h': float(data['priceChangePercent']),
            'volume_24h': float(data['volume']),
            'high_24h': float(data['highPrice']),
            'low_24h': float(data['lowPrice']),
            'source': 'Binance',
            'timestamp': datetime.now().isoformat()
        }

    def _get_from_coingecko(self) -> Dict:
        """Get price from CoinGecko API (backup)"""
        url = f"{self.coingecko_url}/simple/price"
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_24hr_vol': 'true'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()['bitcoin']

        return {
            'price': float(data['usd']),
            'price_change_24h': float(data.get('usd_24h_change', 0)),
            'volume_24h': float(data.get('usd_24h_vol', 0)),
            'high_24h': None,  # CoinGecko free tier doesn't include this
            'low_24h': None,
            'source': 'CoinGecko',
            'timestamp': datetime.now().isoformat()
        }

    def _get_from_coincap(self) -> Dict:
        """Get price from CoinCap API (backup 2)"""
        url = f"{self.coincap_url}/assets/bitcoin"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()['data']

        return {
            'price': float(data['priceUsd']),
            'price_change_24h': float(data.get('changePercent24Hr', 0)),
            'volume_24h': float(data.get('volumeUsd24Hr', 0)),
            'high_24h': None,
            'low_24h': None,
            'source': 'CoinCap',
            'timestamp': datetime.now().isoformat()
        }

    def get_historical_data(self, interval: str = '1h', limit: int = 100) -> List[Dict]:
        """
        Get historical candlestick data for RSI calculation.

        Args:
            interval: '1m', '5m', '15m', '1h', '4h', '1d'
            limit: Number of candles (max 1000)

        Returns:
            List of candle dictionaries

        Note: Only available from Binance. Falls back to empty if unavailable.
        """
        try:
            url = f"{self.binance_url}/klines"
            params = {
                'symbol': 'BTCUSDT',
                'interval': interval,
                'limit': limit
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            candles = response.json()

            return [
                {
                    'timestamp': candle[0],
                    'open': float(candle[1]),
                    'high': float(candle[2]),
                    'low': float(candle[3]),
                    'close': float(candle[4]),
                    'volume': float(candle[5])
                }
                for candle in candles
            ]
        except Exception as e:
            print(f"Warning: Could not fetch historical data: {e}")
            print("Historical data (for RSI) requires Binance API")
            return []


# Backward compatibility
class BinanceConnector(BitcoinPriceConnector):
    """Alias for backward compatibility"""
    pass
