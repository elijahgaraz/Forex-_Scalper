"""Trading interface for IC Markets (cTrader)."""
from typing import List, Optional

# Placeholder for actual cTrader API integration
class Trader:
    def __init__(self, settings):
        self.settings = settings

    def open_trade(self, symbol: str, volume: float, direction: str, stop_loss: Optional[float] = None, take_profit: Optional[float] = None):
        """Open a trade. Direction should be 'buy' or 'sell'."""
        # Input validation
        if not isinstance(symbol, str) or not symbol.strip():
            raise ValueError("Symbol must be a non-empty string.")
        if direction not in ('buy', 'sell'):
            raise ValueError("Direction must be 'buy' or 'sell'.")
        if not isinstance(volume, (int, float)) or volume <= 0:
            raise ValueError("Volume must be a positive number.")
        if stop_loss is not None and not isinstance(stop_loss, (int, float)):
            raise ValueError("Stop-Loss must be a number or None.")
        if take_profit is not None and not isinstance(take_profit, (int, float)):
            raise ValueError("Take-Profit must be a number or None.")

        # Further validation for SL/TP values (e.g., SL for buy must be < current price)
        # would go here once price data is available.

        trade_details = f"Opening {direction} trade on {symbol} with volume {volume}"
        if stop_loss is not None:
            trade_details += f", SL: {stop_loss}"
        if take_profit is not None:
            trade_details += f", TP: {take_profit}"

        print(trade_details)
        # TODO: integrate with cTrader API using all parameters including SL/TP

    def close_trade(self, trade_id: str):
        print(f"Closing trade {trade_id}")
        # TODO: integrate with cTrader API

    def get_open_trades(self) -> List[dict]:
        print("Fetching open trades")
        return []

    def get_account_info(self) -> dict:
        print("Fetching account info")
        return {}
