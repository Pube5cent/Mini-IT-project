import os
import json

DEFAULT_ITEMS = {
    "Book Seller": {
        "cost": 12,
        "owned": 0,
        "cps": 0.5,
        "elapsed": 0.0,
        "gif_path": "AdamStuff/assets/book_seller.gif"
    },
    "Student": {
        "cost": 100,
        "owned": 0,
        "cps": 2,
        "elapsed": 0.0,
        "gif_path": "AdamStuff/assets/student.gif"
    }
}

SAVE_FILE = "save_data.json"

def save_game(Knowledge, player_state, items):
    for item in items.values():
        if "frames" in item:
            del item["frames"]  # Don't save Pygame surfaces
    with open(SAVE_FILE, "w") as f:
        json.dump({
            "Knowledge": Knowledge,
            "player_state": player_state,
            "items": items
        }, f, indent=4)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        Knowledge = data.get("Knowledge", 0)
        player_state = data.get("player_state", {})
        saved_items = data.get("items", {})

        # Ensure every default item exists and has all required keys
        items = {}
        for name, defaults in DEFAULT_ITEMS.items():
            saved = saved_items.get(name, {})
            combined = defaults.copy()
            combined.update(saved)  # saved values override defaults
            items[name] = combined

        return Knowledge, player_state, items

    # If no save file, return default values
    return 0, {}, DEFAULT_ITEMS.copy()
