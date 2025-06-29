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


class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding="10 10 10 10")

        ttk.Label(self, text="Application Settings", font=("Arial", 16, "bold")).pack(pady=(0,15))

        # --- Environment Selection ---
        env_frame = ttk.Frame(self)
        env_frame.pack(fill="x", pady=5)

        ttk.Label(env_frame, text="Active Environment:").pack(side="left", padx=(0,10))
        self.environment_var = tk.StringVar(value=self.controller.settings.active_environment.capitalize())
        self.environment_cb = ttk.Combobox(
            env_frame,
            textvariable=self.environment_var,
            values=["Demo", "Live"],
            state="readonly"
        )
        self.environment_cb.pack(side="left")
        self.environment_cb.bind("<<ComboboxSelected>>", self.on_environment_change)

        # --- Credentials Frame ---
        # Using Labelframe for better visual grouping of credentials
        credentials_frame = ttk.Labelframe(self, text="Environment Credentials", padding="10")
        credentials_frame.pack(fill="x", expand=True, pady=10)

        # API Key
        ttk.Label(credentials_frame, text="API Key:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(credentials_frame, textvariable=self.api_key_var, width=50)
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Account ID
        ttk.Label(credentials_frame, text="Account ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.account_id_var = tk.StringVar()
        self.account_id_entry = ttk.Entry(credentials_frame, textvariable=self.account_id_var, width=50)
        self.account_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Broker URL
        ttk.Label(credentials_frame, text="Broker URL:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.broker_url_var = tk.StringVar()
        self.broker_url_entry = ttk.Entry(credentials_frame, textvariable=self.broker_url_var, width=50)
        self.broker_url_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        credentials_frame.columnconfigure(1, weight=1) # Make entry fields expand

        # --- Action Buttons ---
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", pady=10)

        self.save_button = ttk.Button(action_frame, text="Save Settings", command=self.save_settings, style="Accent.TButton")
        self.save_button.pack(side="left", padx=5)

        self.back_button = ttk.Button(action_frame, text="Back to Trading", command=lambda: controller.show_frame("TradingPage"))
        self.back_button.pack(side="right", padx=5)

        # Load initial values when frame is created
        self.load_current_environment_settings()

    def load_current_environment_settings(self):
        """Loads credentials into UI fields based on selected environment."""
        env = self.environment_var.get().lower() # 'demo' or 'live'
        settings = self.controller.settings

        if env == 'demo':
            self.api_key_var.set(settings.demo_api_key)
            self.account_id_var.set(settings.demo_account_id)
            self.broker_url_var.set(settings.demo_broker_url)
        elif env == 'live':
            self.api_key_var.set(settings.live_api_key)
            self.account_id_var.set(settings.live_account_id)
            self.broker_url_var.set(settings.live_broker_url)

    def on_environment_change(self, event=None):
        """Handles environment selection change."""
        # First, save any pending changes to the *previously* selected environment
        # This is a bit complex if we want to save before switching.
        # For simplicity now, we can prompt user or just load.
        # Let's just load for now. A more robust solution might ask to save current changes.
        self.load_current_environment_settings()
        # The active_environment in actual settings will be updated on Save.

    def save_settings(self):
        """Saves the currently displayed credentials to the selected environment in settings."""
        env = self.environment_var.get().lower()
        settings = self.controller.settings

        settings.active_environment = env # Update active environment

        api_key = self.api_key_var.get()
        account_id = self.account_id_var.get()
        broker_url = self.broker_url_var.get()

        if env == 'demo':
            settings.demo_api_key = api_key
            settings.demo_account_id = account_id
            settings.demo_broker_url = broker_url
        elif env == 'live':
            settings.live_api_key = api_key
            settings.live_account_id = account_id
            settings.live_broker_url = broker_url

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
