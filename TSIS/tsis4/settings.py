"""
settings.py — load / save user preferences from settings.json
"""

import json
import os
from config import SETTINGS_FILE

# ---------- DEFAULTS ----------
_DEFAULTS = {
    "snake_color": [0, 200, 0],   # RGB list (JSON-serialisable)
    "grid_overlay": True,
    "sound": True,
}


def load() -> dict:
    """Return settings dict, falling back to defaults for missing keys."""
    if not os.path.exists(SETTINGS_FILE):
        return dict(_DEFAULTS)

    try:
        with open(SETTINGS_FILE, "r") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULTS)

    # Fill in any keys that may be missing from an older save.
    for key, value in _DEFAULTS.items():
        data.setdefault(key, value)

    return data


def save(settings: dict) -> None:
    with open(SETTINGS_FILE, "w") as fh:
        json.dump(settings, fh, indent=2)