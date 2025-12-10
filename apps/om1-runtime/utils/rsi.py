"""
RSI (Relative Strength Index) Calculation Utilities

Standard 14-period RSI calculation for Bitcoin price analysis.
"""

import numpy as np
from typing import List, Dict, Union


def calculate_rsi(prices: Union[List[float], List[Dict]], period: int = 14) -> float:
    """
    Calculate RSI using standard 14-period formula.

    Args:
        prices: List of prices (floats) or list of candle dicts with 'close'
        period: RSI period (default: 14)

    Returns:
        RSI value (0-100)
    """
    # Extract close prices if candles dict provided
    if isinstance(prices[0], dict):
        prices = [candle['close'] for candle in prices]

    if len(prices) < period + 1:
        return 50.0  # Neutral default if insufficient data

    # Convert to numpy array
    prices = np.array(prices, dtype=float)

    # Calculate price changes
    deltas = np.diff(prices)

    # Separate gains and losses
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    # Calculate average gains and losses
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    # Calculate subsequent average gains/losses using smoothing
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    # Avoid division by zero
    if avg_loss == 0:
        return 100.0

    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return float(rsi)


def interpret_rsi(rsi: float) -> str:
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
