"""Application settings and credential management."""
from dataclasses import dataclass, field
from typing import Optional
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

@dataclass
class Settings:
    api_key: str = ''
    account_id: str = ''
    broker_url: str = 'https://api.icmarkets.com'

    @classmethod
    def load(cls) -> 'Settings':
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                return cls(**data)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {CONFIG_FILE}. Using default settings.")
            except Exception as e:
                print(f"Warning: Could not load settings from {CONFIG_FILE} due to {e}. Using default settings.")
        return cls()

    def save(self) -> None:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
