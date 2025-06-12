import time
import json
import os

SAVE_FILE = "save_data.json"

def save_game(Knowledge, rebirth_multiplier, rebirth_count, upgrades):
    data = {
        "Knowledge": Knowledge,
        "rebirth_multiplier": rebirth_multiplier,
        "rebirth_count": rebirth_count,
        "upgrade_levels": [u["level"] for u in upgrades],
        "last_saved_time": time.time()
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_game(upgrades):
    if not os.path.exists(SAVE_FILE):
        return 0, 1, 0, time.time()  # default: 0 knowledge, x1 multiplier, 0 rebirths

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        Knowledge = data.get("Knowledge", 0)
        multiplier = data.get("rebirth_multiplier", 1)
        count = data.get("rebirth_count", 0)
        last_saved_time = data.get("last_saved_time", time.time())
        upgrade_levels = data.get("upgrade_levels", [])

        for i, level in enumerate(upgrade_levels):
            if i < len(upgrades):
                upgrades[i]["level"] = level

        return Knowledge, multiplier, count, last_saved_time

    except Exception as e:
        print("Failed to load save:", e)
        return 0, 1, 0, time.time()