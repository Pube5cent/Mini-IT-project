import json
import time
import os

def save_game(Knowledge, Insight, Rebirth_multiplier, items, filename="save.json"):
    data = {
        "knowledge": Knowledge,
        "insight": Insight,
        "rebirth_multiplier": Rebirth_multiplier,
        "items": {name: {"owned": item["owned"]} for name, item in items.items()},
        "last_time": time.time()
    }
    with open(filename, "w") as f:
        json.dump(data, f)

def load_game(items, filename="save.json"):
    Knowledge = 0
    Insight = 0
    Rebirth_multiplier = 1.0
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)

        Knowledge = data.get("knowledge", 0)
        Insight = data.get("insight", 0)
        Rebirth_multiplier = data.get("rebirth_multiplier", 1.0)
        last_time = data.get("last_time", time.time())
        offline_seconds = time.time() - last_time

        for name, item_data in data.get("items", {}).items():
            if name in items:
                items[name]["owned"] = item_data["owned"]

        # Calculate offline Knowledge earned
        for item in items.values():
            if item["cps"] > 0 and item["owned"] > 0:
                Knowledge += item["cps"] * item["owned"] * offline_seconds * Rebirth_multiplier

    return Knowledge, Insight, Rebirth_multiplier
