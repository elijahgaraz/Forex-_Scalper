"""Trading interface for IC Markets (cTrader)."""
from typing import List, Optional
import threading
import time
import uuid

# Placeholder for actual cTrader API integration
class Trader:
    def __init__(self, settings_obj: 'Settings'): # Type hint with quotes for forward reference
        self.settings = settings_obj

        # Store FIX connection parameters from settings
        self.fix_host = self.settings.fix_host
        self.fix_port = self.settings.fix_port
        self.fix_sender_comp_id = self.settings.fix_sender_comp_id
        self.fix_target_comp_id = self.settings.fix_target_comp_id
        self.fix_sender_sub_id = self.settings.fix_sender_sub_id
        self.fix_password = self.settings.fix_password # Be mindful of using/logging this

        self.mode = "FIX Live" # Indicate current configuration type

        # Connection state and account summary
        self.is_connected: bool = False
        self.connection_message: str = "Disconnected"
        # Unique identifier of the trading account (using SenderCompID as a stand-in)
        self.account_id: str = ""
        # Example structure, can be expanded based on actual data from FIX
        self.account_summary: dict = {
            'balance': 0.0,
            'equity': 0.0,
            'margin': 0.0,
        }

        # Track open trades
        self.open_trades: List[dict] = []
        self._trade_counter: int = 1

        # Heartbeat thread management
        self._running: bool = False
        self._heartbeat_thread: Optional[threading.Thread] = None

        print(f"Trader initialized for {self.mode} connection.")
        print(f"  Host: {self.fix_host}:{self.fix_port}")
        print(f"  SenderCompID: {self.fix_sender_comp_id}")
        print(f"  TargetCompID: {self.fix_target_comp_id}")
        # Actual FIX client (e.g., QuickFIX) would be initialized and configured here.
        # For now, this is just a placeholder update.

    def connect(self) -> bool:
        """
        Placeholder for establishing a FIX connection.
        Simulates connection success/failure.
        """
        print(f"[{self.mode}] Attempting to connect...")
        # Simulate connection logic: success if SenderCompID is set
        if not self.fix_sender_comp_id:
            self.is_connected = False
            self.connection_message = "Connection Failed: SenderCompID is not set."
            print(self.connection_message)
            return False

        if not self.fix_password: # Basic check, real FIX logon is more complex
            self.is_connected = False
            self.connection_message = "Connection Failed: Password is not set."
            print(self.connection_message)
            return False

        # Simulate successful connection
        self.is_connected = True
        self.connection_message = "Connected"
        self.account_id = self.fix_sender_comp_id  # Mock retrieval of account id
        self.account_summary = {
            'balance': 10000.00,
            'equity': 10500.50,
            'margin': 150.25,
        }  # Mock data
        print(f"[{self.mode}] Successfully connected. Account Summary: {self.account_summary}")
        return True

    def disconnect(self) -> None:
        """
        Placeholder for closing a FIX connection.
        """
        print(f"[{self.mode}] Attempting to disconnect...")
        self.is_connected = False
        self.connection_message = "Disconnected"
        self.account_id = ""
        self.account_summary = {
            'balance': 0.0,
            'equity': 0.0,
            'margin': 0.0,
        }  # Clear data
        print(f"[{self.mode}] Successfully disconnected.")

    def get_connection_status(self) -> tuple[bool, str]:
        """Returns the current connection status and message."""
        return self.is_connected, self.connection_message

    def get_account_summary(self) -> dict:
        """Returns the current account summary data."""
        return self.account_summary.copy() # Return a copy to prevent external modification

    def open_trade(self, symbol: str, volume: float, direction: str, stop_loss: Optional[float] = None, take_profit: Optional[float] = None):
        """Open a trade. Direction should be 'buy' or 'sell'."""
        # Input validation (remains the same for now)
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

        trade_details = f"[{self.mode}] Attempting to open {direction} trade on {symbol} with volume {volume}"
        if stop_loss is not None:
            trade_details += f", SL: {stop_loss}"
        if take_profit is not None:
            trade_details += f", TP: {take_profit}"

        print(trade_details)
        print(f"  (Using SenderCompID: {self.fix_sender_comp_id})")

        trade_id = f"T{self._trade_counter:06d}"
        self._trade_counter += 1
        trade = {
            'id': trade_id,
            'symbol': symbol,
            'volume': volume,
            'direction': direction,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
        }
        self.open_trades.append(trade)
        print(f"[{self.mode}] Trade {trade_id} opened.")
        return trade_id

    def close_trade(self, trade_id: str):
        print(f"[{self.mode}] Attempting to close trade {trade_id} (SenderCompID: {self.fix_sender_comp_id})")
        for trade in list(self.open_trades):
            if trade['id'] == trade_id:
                self.open_trades.remove(trade)
                print(f"[{self.mode}] Trade {trade_id} closed.")
                return True
        print(f"[{self.mode}] Trade {trade_id} not found.")
        return False

    def get_open_trades(self) -> List[dict]:
        print(f"[{self.mode}] Fetching open trades (SenderCompID: {self.fix_sender_comp_id})")
        return list(self.open_trades)

    def get_account_info(self) -> dict:
        print(f"[{self.mode}] Fetching account info (SenderCompID: {self.fix_sender_comp_id})")
        info = self.get_account_summary()
        info['account_id'] = self.account_id or self.fix_sender_comp_id
        return info

    def start_heartbeat(self, interval: float = 30.0) -> None:
        """Start a background thread that maintains the connection."""
        if self._running:
            return

        self._running = True

        def _heartbeat_loop() -> None:
            while self._running:
                if not self.is_connected:
                    self.connect()
                time.sleep(interval)

        self._heartbeat_thread = threading.Thread(target=_heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()

    def stop_heartbeat(self) -> None:
        """Stop the background heartbeat thread."""
        self._running = False
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join(timeout=1)
