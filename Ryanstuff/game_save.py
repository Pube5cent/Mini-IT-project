import json
import time
import os

def save_game(Knowledge, Insight, rebirth_system, items, filename="save.json"):
    data = {
        "knowledge": Knowledge,
        "insight": Insight,
        "rebirth_multiplier": rebirth_system.multiplier,
        "rebirth_count": rebirth_system.rebirth_count,
        "items": {
            name: {
                "owned": item["owned"],
                "cost": item["cost"],
                "click_bonus": item.get("click_bonus", 0)
            } for name, item in items.items()
        },
        "last_time": time.time()
    }
    with open(filename, "w") as f:
        json.dump(data, f)


def load_game(items, filename="save.json"):
    Knowledge = 0
    Insight = 0
    rebirth_multiplier = 1.0
    rebirth_count = 0

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)

        Knowledge = data.get("knowledge", 0)
        Insight = data.get("insight", 0)
        rebirth_multiplier = data.get("rebirth_multiplier", 1.0)
        rebirth_count = data.get("rebirth_count", 0)
        last_time = data.get("last_time", time.time())
        offline_seconds = time.time() - last_time

        saved_items = data.get("items", {})
        for name, item_data in saved_items.items():
            if name in items:
                items[name]["owned"] = item_data.get("owned", 0)
                items[name]["cost"] = item_data.get("cost", items[name]["cost"])
                if "click_bonus" in items[name]:
                    items[name]["click_bonus"] = item_data.get("click_bonus", 0)

        for item in items.values():
            if item["cps"] > 0 and item["owned"] > 0:
                Knowledge += item["cps"] * item["owned"] * offline_seconds * rebirth_multiplier

    return Knowledge, Insight, rebirth_multiplier, rebirth_count
