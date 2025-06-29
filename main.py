"""Entry point for the Forex Scalper application."""
from .gui import MainApplication

def main() -> None:
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()
