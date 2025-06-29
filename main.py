"""Entry point for the Forex Scalper application."""
import sys
import os

# Add the project root to sys.path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from gui import MainApplication

def main() -> None:
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()
