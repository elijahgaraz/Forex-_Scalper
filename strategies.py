"""AI trading strategies."""
from abc import ABC, abstractmethod
from typing import Any, Sequence
from statistics import mean

class Strategy(ABC):
    """Abstract base class for trading strategies."""

    @abstractmethod
    def decide(self, market_data: Any) -> str:
        """Return 'buy', 'sell', or 'hold'."""
        pass


def _sma(values: Sequence[float], window: int) -> float:
    if len(values) < window:
        return mean(values)
    return mean(values[-window:])

class SafeStrategy(Strategy):
    def decide(self, market_data: Any) -> str:
        """Conservative strategy using a long-term moving average."""
        prices = market_data.get('prices', []) if isinstance(market_data, dict) else []
        if len(prices) < 2:
            return 'hold'
        short = _sma(prices, 20)
        long = _sma(prices, 50)
        if short > long:
            return 'buy'
        if short < long:
            return 'sell'
        return 'hold'

class ModerateStrategy(Strategy):
    def decide(self, market_data: Any) -> str:
        """Balanced strategy with shorter averages."""
        prices = market_data.get('prices', []) if isinstance(market_data, dict) else []
        if len(prices) < 2:
            return 'hold'
        short = _sma(prices, 10)
        long = _sma(prices, 30)
        if short > long:
            return 'buy'
        if short < long:
            return 'sell'
        return 'hold'

class AggressiveStrategy(Strategy):
    def decide(self, market_data: Any) -> str:
        """Aggressive strategy reacting quickly to price changes."""
        prices = market_data.get('prices', []) if isinstance(market_data, dict) else []
        if len(prices) < 2:
            return 'hold'
        short = _sma(prices, 5)
        long = _sma(prices, 15)
        if short > long:
            return 'buy'
        if short < long:
            return 'sell'
        return 'hold'
