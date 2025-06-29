"""Tkinter GUI for the scalping application."""
import tkinter as tk
from tkinter import ttk
from settings import Settings
from trading import Trader
from strategies import SafeStrategy, ModerateStrategy, AggressiveStrategy


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Forex Scalper")
        self.geometry("600x400")

        self.settings = Settings.load()
        # The Trader instance is initialized with the settings loaded at startup.
        # If active_environment is changed in settings, the application
        # currently needs to be restarted for the Trader to use the new environment.
        self.trader = Trader(self.settings)
        # Maintain a background connection to allow unattended operation
        self.trader.start_heartbeat()

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (TradingPage, SettingsPage, ActivityPage):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TradingPage")

    def show_frame(self, name: str):
        frame = self.frames[name]
        frame.tkraise()


class TradingPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding="10 10 10 10")

        # Main page title (optional, could be part of window title)
        # page_title = ttk.Label(self, text="Trading Dashboard", font=("Arial", 16, "bold"))
        # page_title.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # --- Trade Parameters Frame ---
        trade_params_frame = ttk.Labelframe(self, text="Trade Parameters", padding="10 10 10 10")
        trade_params_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Symbol
        ttk.Label(trade_params_frame, text="Symbol (e.g., EURUSD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.symbol_var = tk.StringVar()
        self.symbol_entry = ttk.Entry(trade_params_frame, textvariable=self.symbol_var, width=15)
        self.symbol_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Volume
        ttk.Label(trade_params_frame, text="Volume (lots):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.volume_var = tk.StringVar()
        self.volume_entry = ttk.Entry(trade_params_frame, textvariable=self.volume_var, width=15)
        self.volume_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Stop-Loss
        ttk.Label(trade_params_frame, text="Stop-Loss (price):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.stop_loss_var = tk.StringVar()
        self.stop_loss_entry = ttk.Entry(trade_params_frame, textvariable=self.stop_loss_var, width=15)
        self.stop_loss_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Take-Profit
        ttk.Label(trade_params_frame, text="Take-Profit (price):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.take_profit_var = tk.StringVar()
        self.take_profit_entry = ttk.Entry(trade_params_frame, textvariable=self.take_profit_var, width=15)
        self.take_profit_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        trade_params_frame.columnconfigure(1, weight=1) # Make entry fields expand

        # --- Strategy & Actions Frame ---
        strategy_actions_frame = ttk.Labelframe(self, text="Strategy & Actions", padding="10 10 10 10")
        strategy_actions_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        ttk.Label(strategy_actions_frame, text="Select Strategy:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.strategy_var = tk.StringVar()
        self.strategy_combobox = ttk.Combobox(
            strategy_actions_frame,
            textvariable=self.strategy_var,
            values=["SafeStrategy", "ModerateStrategy", "AggressiveStrategy"],
            width=20
        )
        self.strategy_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.strategy_combobox.set("SafeStrategy")  # Default value

        self.execute_trade_button = ttk.Button(strategy_actions_frame, text="Execute Trade", command=self.execute_trade, style="Accent.TButton") # Using a potential custom style
        self.execute_trade_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        strategy_actions_frame.columnconfigure(1, weight=1)

        # --- Navigation Buttons Frame ---
        nav_frame = ttk.Frame(self, padding="5 5 5 5")
        nav_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        self.settings_button = ttk.Button(nav_frame, text="Settings", command=lambda: controller.show_frame("SettingsPage"))
        self.settings_button.pack(side="left", padx=5)

        self.activity_button = ttk.Button(nav_frame, text="Activity Log", command=lambda: controller.show_frame("ActivityPage"))
        self.activity_button.pack(side="left", padx=5)

        # --- Feedback Label ---
        self.feedback_label = ttk.Label(self, text="", anchor="center")
        self.feedback_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # --- Account Info Frame ---
        account_frame = ttk.Labelframe(self, text="Account Info", padding="10 10 10 10")
        account_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.account_id_label = ttk.Label(account_frame, text="Account ID: -")
        self.account_id_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        self.balance_label = ttk.Label(account_frame, text="Balance: -")
        self.balance_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.equity_label = ttk.Label(account_frame, text="Equity: -")
        self.equity_label.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        self.margin_label = ttk.Label(account_frame, text="Margin: -")
        self.margin_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        account_frame.columnconfigure(1, weight=1)

        # start periodic account info updates
        self.update_account_info()

        # Configure column weights for resizing behavior of the main TradingPage frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        # self.rowconfigure(0, weight=1) # If you want frames to expand vertically too

    def execute_trade(self):
        symbol = self.symbol_var.get().strip().upper()
        volume_str = self.volume_var.get().strip()
        stop_loss_str = self.stop_loss_var.get().strip()
        take_profit_str = self.take_profit_var.get().strip()

        # Validation
        if not symbol:
            self.feedback_label.config(text="Symbol cannot be empty.", foreground="red")
            return

        try:
            volume = float(volume_str)
            if volume <= 0:
                raise ValueError("Volume must be positive.")
        except ValueError:
            self.feedback_label.config(text="Invalid volume. Must be a positive number.", foreground="red")
            return

        stop_loss = None
        if stop_loss_str:
            try:
                stop_loss = float(stop_loss_str)
            except ValueError:
                self.feedback_label.config(text="Invalid Stop-Loss. Must be a number or empty.", foreground="red")
                return

        take_profit = None
        if take_profit_str:
            try:
                take_profit = float(take_profit_str)
            except ValueError:
                self.feedback_label.config(text="Invalid Take-Profit. Must be a number or empty.", foreground="red")
                return

        selected_strategy_name = self.strategy_var.get()
        strategy_class_map = {
            "SafeStrategy": SafeStrategy,
            "ModerateStrategy": ModerateStrategy,
            "AggressiveStrategy": AggressiveStrategy
        }

        strategy_class = strategy_class_map.get(selected_strategy_name)
        if not strategy_class: # Should not happen with Combobox
            self.feedback_label.config(text="Invalid strategy selected.", foreground="red")
            return

        strategy = strategy_class()
        # Market data is still None. In a real scenario, this would be fetched or passed.
        # Potentially, symbol could be used to fetch relevant market data.
        decision = strategy.decide(market_data=None)

        if decision in ("buy", "sell"):
            try:
                self.controller.trader.open_trade(
                    symbol=symbol,
                    volume=volume,
                    direction=decision,
                    stop_loss=stop_loss,
                    take_profit=take_profit
                )
                self.feedback_label.config(
                    text=f"Trade {decision.capitalize()} {volume} of {symbol} initiated.",
                    foreground="green"
                )
            except ValueError as ve: # Catch specific validation errors from Trader
                self.feedback_label.config(text=f"Trade failed: {ve}", foreground="red")
            except Exception as e: # Catch other unexpected errors
                self.feedback_label.config(text=f"Trade failed: An unexpected error occurred - {e}", foreground="red")
        else: # 'hold' or other decision
            self.feedback_label.config(text=f"No trade executed: Strategy decided to '{decision}'.", foreground="orange")

    def update_account_info(self):
        """Refresh displayed account details."""
        is_connected, _ = self.controller.trader.get_connection_status()
        if is_connected:
            info = self.controller.trader.get_account_info()
            self.account_id_label.config(text=f"Account ID: {info.get('account_id', '-')}")
            self.balance_label.config(text=f"Balance: {info.get('balance', 0):.2f}")
            self.equity_label.config(text=f"Equity: {info.get('equity', 0):.2f}")
            self.margin_label.config(text=f"Margin: {info.get('margin', 0):.2f}")
        else:
            self.account_id_label.config(text="Account ID: -")
            self.balance_label.config(text="Balance: -")
            self.equity_label.config(text="Equity: -")
            self.margin_label.config(text="Margin: -")
        # schedule next update
        self.after(5000, self.update_account_info)


class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding="10 10 10 10")

        ttk.Label(self, text="FIX Connection Settings", font=("Arial", 16, "bold")).pack(pady=(0,15))

        # --- Credentials Frame ---
        credentials_frame = ttk.Labelframe(self, text="Live FIX Credentials", padding="10")
        credentials_frame.pack(fill="x", expand=True, pady=10)

        # FIX Host
        ttk.Label(credentials_frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.fix_host_var = tk.StringVar()
        self.fix_host_entry = ttk.Entry(credentials_frame, textvariable=self.fix_host_var, width=40)
        self.fix_host_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # FIX Port
        ttk.Label(credentials_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.fix_port_var = tk.StringVar() # Store as string for Entry, convert on save
        self.fix_port_entry = ttk.Entry(credentials_frame, textvariable=self.fix_port_var, width=10)
        self.fix_port_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w") # sticky w for short field

        # FIX SenderCompID
        ttk.Label(credentials_frame, text="SenderCompID:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.fix_sender_comp_id_var = tk.StringVar()
        self.fix_sender_comp_id_entry = ttk.Entry(credentials_frame, textvariable=self.fix_sender_comp_id_var, width=40)
        self.fix_sender_comp_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # FIX TargetCompID
        ttk.Label(credentials_frame, text="TargetCompID:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.fix_target_comp_id_var = tk.StringVar()
        self.fix_target_comp_id_entry = ttk.Entry(credentials_frame, textvariable=self.fix_target_comp_id_var, width=40)
        self.fix_target_comp_id_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # FIX SenderSubID
        ttk.Label(credentials_frame, text="SenderSubID:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.fix_sender_sub_id_var = tk.StringVar()
        self.fix_sender_sub_id_entry = ttk.Entry(credentials_frame, textvariable=self.fix_sender_sub_id_var, width=40)
        self.fix_sender_sub_id_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # FIX Password
        ttk.Label(credentials_frame, text="Password:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.fix_password_var = tk.StringVar()
        self.fix_password_entry = ttk.Entry(credentials_frame, textvariable=self.fix_password_var, width=40, show='*')
        self.fix_password_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        credentials_frame.columnconfigure(1, weight=1) # Make entry fields expand (except port)

        # --- Action Buttons ---
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", pady=10)

        self.save_button = ttk.Button(action_frame, text="Save Settings", command=self.save_settings, style="Accent.TButton")
        self.save_button.pack(side="left", padx=5)

        self.back_button = ttk.Button(action_frame, text="Back to Trading", command=lambda: controller.show_frame("TradingPage"))
        self.back_button.pack(side="right", padx=5)

        # Load initial values when frame is created
        self.load_fix_settings()

    def load_fix_settings(self):
        """Loads FIX credentials into UI fields."""
        settings = self.controller.settings
        self.fix_host_var.set(settings.fix_host)
        self.fix_port_var.set(str(settings.fix_port)) # Port is int in settings, str for Entry
        self.fix_sender_comp_id_var.set(settings.fix_sender_comp_id)
        self.fix_target_comp_id_var.set(settings.fix_target_comp_id)
        self.fix_sender_sub_id_var.set(settings.fix_sender_sub_id)
        self.fix_password_var.set(settings.fix_password)

    # on_environment_change method is no longer needed as there's no environment selection
    # def on_environment_change(self, event=None):
    #     pass

    def save_settings(self):
        """Saves the FIX credentials from UI fields to the Settings object."""
        settings = self.controller.settings

        settings.fix_host = self.fix_host_var.get()
        try:
            settings.fix_port = int(self.fix_port_var.get())
        except ValueError:
            # Handle error: port must be an integer.
            # For now, print warning and don't save invalid port.
            # A more robust solution would show a message in the UI.
            print(f"Warning: Invalid port number '{self.fix_port_var.get()}'. Port not saved.")
            # Optionally, could revert fix_port_var to original value or highlight error.

        settings.fix_sender_comp_id = self.fix_sender_comp_id_var.get()
        settings.fix_target_comp_id = self.fix_target_comp_id_var.get()
        settings.fix_sender_sub_id = self.fix_sender_sub_id_var.get()
        settings.fix_password = self.fix_password_var.get()

        settings.save()
        # Optionally, provide feedback to the user
        # For example, using the TradingPage's feedback label if we passed a reference
        # or adding a temporary status label to SettingsPage itself.
        print("Settings saved.") # Placeholder feedback

class ActivityPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Activity Page").pack(pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame("TradingPage")).pack()
        self.output = tk.Text(self, height=15)
        self.output.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        trades = self.controller.trader.get_open_trades()
        self.output.delete("1.0", tk.END)
        for trade in trades:
            self.output.insert(tk.END, f"{trade}\n")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
