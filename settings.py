"""Application settings and credential management."""
from dataclasses import dataclass, field
from typing import Optional
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

@dataclass
class Settings:
    # FIX connection parameters (assuming single, live configuration)
    fix_host: str = 'live-uk-eqx-01.p.c-trader.com'
    fix_port: int = 5212
    fix_sender_comp_id: str = ''  # User specific, e.g., 'live4.icmarkets.6077021'
    fix_target_comp_id: str = 'cServer'
    fix_sender_sub_id: str = 'TRADE'
    fix_password: str = ''        # User specific

    # __post_init__ is removed as migration logic for old fields is no longer complex;
    # old fields are entirely removed. Load method will handle missing new fields from very old configs.

    @classmethod
    def load(cls) -> 'Settings':
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)

                # Populate with data from file, using defaults if keys are missing
                # This handles loading an older config that might not have all these fields
                settings_data = {
                    'fix_host': data.get('fix_host', 'live-uk-eqx-01.p.c-trader.com'),
                    'fix_port': data.get('fix_port', 5212),
                    'fix_sender_comp_id': data.get('fix_sender_comp_id', ''),
                    'fix_target_comp_id': data.get('fix_target_comp_id', 'cServer'),
                    'fix_sender_sub_id': data.get('fix_sender_sub_id', 'TRADE'),
                    'fix_password': data.get('fix_password', '')
                }
                return cls(**settings_data)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {CONFIG_FILE}. Using default settings.")
            except Exception as e:
                print(f"Warning: Could not load settings from {CONFIG_FILE} due to {e}. Using default settings.")
        # If config file doesn't exist or fails to load, return instance with defaults
        return cls()

    def save(self) -> None:
        # Save all current attributes of the dataclass instance
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
