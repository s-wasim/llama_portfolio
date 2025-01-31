from dotenv import load_dotenv
import os
from typing import List

class PrivateKeys:
    def __init__(self):
        load_dotenv()
        # Store keys in a protected dictionary
        self._keys = {
            'groq': os.getenv('GROQ_API_KEY')
            # Add other keys here as needed
        }

    def __getitem__(self, key: str) -> str:
        if key not in self._keys:
            raise KeyError(f"Key '{key}' not found")
        return self._keys[key]
    
    def __len__(self) -> int:
        return len(self._keys)
    
    def get_key_names(self) -> List[str]:
        """Returns a list of available key names"""
        return list(self._keys.keys())
    
    def has_key(self, key: str) -> bool:
        """Check if a specific key exists"""
        return key in self._keys
