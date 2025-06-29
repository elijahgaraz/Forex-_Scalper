"""Tkinter GUI for the scalping application."""
import tkinter as tk
from tkinter import ttk
from .settings import Settings
from .trading import Trader
from .strategies import SafeStrategy, ModerateStrategy, AggressiveStrategy


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Forex Scalper")
        self.geometry("600x400")

        self.settings = Settings.load()
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
        ttk.Label(self, text="Trading Page").pack(pady=10)
        ttk.Button(self, text="Settings", command=lambda: controller.show_frame("SettingsPage")).pack()
        ttk.Button(self, text="Activity", command=lambda: controller.show_frame("ActivityPage")).pack()
        ttk.Button(self, text="Execute Trade", command=self.execute_trade).pack(pady=20)
        self.feedback_label = ttk.Label(self, text="")
        self.feedback_label.pack(pady=5)

    def execute_trade(self):
        # Dummy example using SafeStrategy
        strategy = SafeStrategy()
        decision = strategy.decide(None)
        if decision in ("buy", "sell"):
            try:
                self.controller.trader.open_trade("EURUSD", 0.01, decision)
                self.feedback_label.config(text="Trade executed successfully!", foreground="green")
            except Exception as e:
                self.feedback_label.config(text=f"Trade failed: {e}", foreground="red")
        else:
            self.feedback_label.config(text="No trade executed: No valid decision.", foreground="orange")


class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Settings Page").pack(pady=10)
        ttk.Label(self, text="API Key").pack()
        self.api_key_entry = ttk.Entry(self)
        self.api_key_entry.insert(0, controller.settings.api_key)
        self.api_key_entry.pack()
        ttk.Button(self, text="Save", command=self.save).pack(pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame("TradingPage")).pack()

    def save(self):
        self.controller.settings.api_key = self.api_key_entry.get()
        self.controller.settings.save()


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
