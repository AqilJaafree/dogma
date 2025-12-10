"""
Bitcoin Price + RSI Input Plugin

Fetches current Bitcoin price and calculates RSI (Relative Strength Index).
"""

from typing import Dict, Any
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from connectors.binance_connector import BitcoinPriceConnector
from utils.rsi import calculate_rsi


class BitcoinPriceInput:
    """
    Input plugin for Bitcoin price data with RSI calculation.

    Fetches from multiple sources (Binance, CoinGecko, CoinCap) with automatic fallback.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Bitcoin price input.

        Args:
            config: Configuration dict with:
                - rsi_period: RSI calculation period (default: 14)
                - sources: List of data sources (default: all)
        """
        self.config = config
        self.rsi_period = config.get('rsi_period', 14)
        self.sources = config.get('sources', ['binance', 'coingecko', 'coincap'])

        self.connector = BitcoinPriceConnector()

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch current Bitcoin price and calculate RSI.

        Returns:
            Dict with:
                - price: Current BTC price in USD
                - rsi: RSI value (0-100)
                - rsi_signal: 'oversold', 'neutral', or 'overbought'
                - price_change_24h: 24-hour price change percentage
                - volume_24h: 24-hour trading volume
                - high_24h: 24-hour high price
                - low_24h: 24-hour low price
                - source: Data source used
                - timestamp: ISO timestamp
        """
        # Fetch current price
        price_data = self.connector.get_current_price()

        # Fetch historical data for RSI
        historical = self.connector.get_historical_data(
            interval='1h',
            limit=self.rsi_period + 1
        )

        # Calculate RSI
        if len(historical) >= self.rsi_period:
            closes = [candle['close'] for candle in historical]
            rsi = calculate_rsi(closes, period=self.rsi_period)
        else:
            rsi = 50.0  # Neutral default if insufficient data

        # Interpret RSI signal
        rsi_signal = self._interpret_rsi(rsi)

        return {
            'price': price_data['price'],
            'rsi': rsi,
            'rsi_signal': rsi_signal,
            'price_change_24h': price_data.get('price_change_24h', 0),
            'volume_24h': price_data.get('volume_24h', 0),
            'high_24h': price_data.get('high_24h'),
            'low_24h': price_data.get('low_24h'),
            'source': price_data['source'],
            'timestamp': price_data['timestamp']
        }

    def _interpret_rsi(self, rsi: float) -> str:
        """
        Interpret RSI value into signal.

        Args:
            rsi: RSI value (0-100)

        Returns:
            'oversold', 'neutral', or 'overbought'
        """
        if rsi < 30:
            return 'oversold'  # Potential buy signal
        elif rsi > 70:
            return 'overbought'  # Potential sell signal
        else:
            return 'neutral'
