"""AI trading strategies."""
from abc import ABC, abstractmethod
from typing import Any

class Strategy(ABC):
    """Abstract base class for trading strategies."""

    @abstractmethod
    def decide(self, market_data: Any) -> str:
        """Return 'buy', 'sell', or 'hold'."""
        pass

class SafeStrategy(Strategy):
    def decide(self, market_data: Any) -> str:
        # Placeholder for a conservative strategy
        return 'hold'

class ModerateStrategy(Strategy):
    def decide(self, market_data: Any) -> str:
        # Placeholder for a balanced strategy
        return 'buy'

class AggressiveStrategy(Strategy):
    def decide(self, market_data: Any) -> str:
        # Placeholder for a high risk strategy
        return 'sell'
