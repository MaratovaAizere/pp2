"""
persistence.py — load/save settings.json and leaderboard.json
Leaderboard keeps only the best score per player (top 10 unique names).
"""

import json, os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE    = "settings.json"
TOP_N            = 10

DEFAULT_SETTINGS = {
    "sound":      True,
    "car_color":  "blue",      # blue | red | green | yellow
    "difficulty": "normal",    # easy | normal | hard
}


# ── Settings ──────────────────────────────────────────────────────────────────

def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                data = json.load(f)
            for k, v in DEFAULT_SETTINGS.items():
                data.setdefault(k, v)
            return data
        except Exception:
            pass
    return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict) -> None:
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


# ── Leaderboard ───────────────────────────────────────────────────────────────

def load_leaderboard() -> list[dict]:
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_leaderboard(new_entry: dict) -> list[dict]:
    """
    Merge new_entry into the stored leaderboard keeping only the best score
    per unique player name, then truncate to TOP_N.
    Returns the updated list.
    """
    entries = load_leaderboard()
    entries.append(new_entry)

    # Keep best score per name
    best: dict[str, dict] = {}
    for e in entries:
        name = e.get("name", "?")
        if name not in best or e["score"] > best[name]["score"]:
            best[name] = e

    result = sorted(best.values(), key=lambda e: e["score"], reverse=True)[:TOP_N]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(result, f, indent=2)
    return result