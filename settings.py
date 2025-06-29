"""Application settings and credential management."""
from dataclasses import dataclass, field
from typing import Optional
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

@dataclass
class Settings:
    # New environment-specific fields
    demo_api_key: str = ''
    demo_account_id: str = ''
    demo_broker_url: str = 'https://ct-api.icmarkets.com/trading/demo' # Example URL
    live_api_key: str = ''
    live_account_id: str = ''
    live_broker_url: str = 'https://ct-api.icmarkets.com/trading/live' # Example URL

    active_environment: str = 'demo'  # 'demo' or 'live'

    # Deprecated generic fields (kept for potential migration)
    api_key: str = ''
    account_id: str = ''
    broker_url: str = ''

    def __post_init__(self):
        # Simple migration: if new fields are empty and old ones have values, migrate.
        # This is a basic approach. A more robust migration might involve versioning.
        if not self.demo_api_key and self.api_key and self.active_environment == 'demo':
            self.demo_api_key = self.api_key
            self.demo_account_id = self.account_id
            self.demo_broker_url = self.broker_url if self.broker_url else 'https://ct-api.icmarkets.com/trading/demo'
            self.api_key = '' # Clear old fields after migration
            self.account_id = ''
            self.broker_url = ''
        elif not self.live_api_key and self.api_key and self.active_environment == 'live':
            # This case is less likely for old configs unless active_environment was somehow set to live
            self.live_api_key = self.api_key
            self.live_account_id = self.account_id
            self.live_broker_url = self.broker_url if self.broker_url else 'https://ct-api.icmarkets.com/trading/live'
            self.api_key = '' # Clear old fields
            self.account_id = ''
            self.broker_url = ''

    @classmethod
    def load(cls) -> 'Settings':
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)

                # Handle potential absence of new fields in older config files
                settings_data = {
                    'demo_api_key': data.get('demo_api_key', data.get('api_key', '') if data.get('active_environment', 'demo') == 'demo' else ''),
                    'demo_account_id': data.get('demo_account_id', data.get('account_id', '') if data.get('active_environment', 'demo') == 'demo' else ''),
                    'demo_broker_url': data.get('demo_broker_url', data.get('broker_url', 'https://ct-api.icmarkets.com/trading/demo') if data.get('active_environment', 'demo') == 'demo' else 'https://ct-api.icmarkets.com/trading/demo'),
                    'live_api_key': data.get('live_api_key', data.get('api_key', '') if data.get('active_environment') == 'live' else ''),
                    'live_account_id': data.get('live_account_id', data.get('account_id', '') if data.get('active_environment') == 'live' else ''),
                    'live_broker_url': data.get('live_broker_url', data.get('broker_url', 'https://ct-api.icmarkets.com/trading/live') if data.get('active_environment') == 'live' else 'https://ct-api.icmarkets.com/trading/live'),
                    'active_environment': data.get('active_environment', 'demo'),
                    # Load deprecated fields too, __post_init__ might use them for migration if new ones are missing
                    'api_key': data.get('api_key', ''),
                    'account_id': data.get('account_id', ''),
                    'broker_url': data.get('broker_url', '')
                }
                return cls(**settings_data)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {CONFIG_FILE}. Using default settings.")
            except Exception as e:
                print(f"Warning: Could not load settings from {CONFIG_FILE} due to {e}. Using default settings.")
        return cls()

    def save(self) -> None:
        # Ensure deprecated fields are not saved if they were cleared by migration
        data_to_save = self.__dict__.copy()
        # We don't need to explicitly remove api_key, account_id, broker_url if they are empty
        # as they are part of the dataclass. Saving them as empty is fine.
        # However, if we wanted to strictly not save them:
        # for key in ['api_key', 'account_id', 'broker_url']:
        #     if not data_to_save.get(key): # if empty or None
        #         data_to_save.pop(key, None)

        with open(CONFIG_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=2)
