"""Trading interface for IC Markets (cTrader)."""
from typing import List, Optional

# Placeholder for actual cTrader API integration
class Trader:
    def __init__(self, settings_obj: 'Settings'): # Type hint with quotes for forward reference
        self.settings = settings_obj # Keep original settings if needed for other things

        if self.settings.active_environment == 'demo':
            self.active_api_key = self.settings.demo_api_key
            self.active_account_id = self.settings.demo_account_id
            self.active_broker_url = self.settings.demo_broker_url
            self.mode = "DEMO"
        elif self.settings.active_environment == 'live':
            self.active_api_key = self.settings.live_api_key
            self.active_account_id = self.settings.live_account_id
            self.active_broker_url = self.settings.live_broker_url
            self.mode = "LIVE"
        else:
            # Default to demo or raise an error if active_environment is invalid
            print(f"Warning: Invalid active_environment '{self.settings.active_environment}'. Defaulting to DEMO mode configuration.")
            self.active_api_key = self.settings.demo_api_key
            self.active_account_id = self.settings.demo_account_id
            self.active_broker_url = self.settings.demo_broker_url
            self.mode = "DEMO (fallback)"

        # For actual API integration, you would initialize your API client here
        # using self.active_api_key, self.active_account_id, self.active_broker_url
        print(f"Trader initialized in {self.mode} mode. URL: {self.active_broker_url}, Account: {self.active_account_id}")


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

        trade_details = f"[{self.mode}] Opening {direction} trade on {symbol} with volume {volume}"
        if stop_loss is not None:
            trade_details += f", SL: {stop_loss}"
        if take_profit is not None:
            trade_details += f", TP: {take_profit}"

        print(trade_details)
        # TODO: integrate with cTrader API using self.active_api_key, self.active_broker_url, etc.

    def close_trade(self, trade_id: str):
        print(f"[{self.mode}] Closing trade {trade_id}")
        # TODO: integrate with cTrader API

    def get_open_trades(self) -> List[dict]:
        print(f"[{self.mode}] Fetching open trades")
        # TODO: integrate with cTrader API
        return []

    def get_account_info(self) -> dict:
        print(f"[{self.mode}] Fetching account info")
        # TODO: integrate with cTrader API
        return {}
