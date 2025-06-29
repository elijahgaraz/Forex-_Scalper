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
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
            return cls(**data)
        return cls()

    def save(self) -> None:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
