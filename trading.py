"""Trading interface for IC Markets (cTrader)."""
from typing import List

# Placeholder for actual cTrader API integration
class Trader:
    def __init__(self, settings):
        self.settings = settings

    def open_trade(self, symbol: str, volume: float, direction: str):
        """Open a trade. Direction should be 'buy' or 'sell'."""
        # Input validation
        if direction not in ('buy', 'sell'):
            raise ValueError("Direction must be 'buy' or 'sell'")
        if not isinstance(volume, (int, float)) or volume <= 0:
            raise ValueError("Volume must be a positive number")
        if not isinstance(symbol, str) or not symbol.strip():
            raise ValueError("Symbol must be a non-empty string")
        print(f"Opening {direction} trade on {symbol} with volume {volume}")
        # TODO: integrate with cTrader API

    def close_trade(self, trade_id: str):
        print(f"Closing trade {trade_id}")
        # TODO: integrate with cTrader API

    def get_open_trades(self) -> List[dict]:
        print("Fetching open trades")
        return []

    def get_account_info(self) -> dict:
        print("Fetching account info")
        return {}
