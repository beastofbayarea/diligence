"""
env_loader.py — load .env file automatically if it exists.

This helps users avoid having to manually export environment variables.
Just call load_env() at the top of your script.
"""

import os
from pathlib import Path


def load_env(path=None):
    """Load .env file from the given path (or repo root if not provided).
    
    Skips lines that are comments (#) or empty, and ignores lines that are
    already set in the environment (environment takes precedence).
    """
    if path is None:
        path = Path(__file__).parent.parent / '.env'
    
    if not os.path.exists(path):
        return False
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                # Environment takes precedence; don't override
                if key not in os.environ:
                    os.environ[key] = val
        return True
    except Exception as e:
        print(f'Warning: failed to load .env: {e}')
        return False
