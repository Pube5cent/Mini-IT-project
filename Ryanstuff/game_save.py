import time
import json

def save_game(Knowledge, rebirth_multiplier, rebirth_count, items):
    # Prepare items for JSON: exclude non-serializable keys like 'frames'
    serializable_items = {}
    for key, val in items.items():
        filtered_val = {k: v for k, v in val.items() if k != "frames"}
        serializable_items[key] = filtered_val

    data = {
        "Knowledge": Knowledge,
        "rebirth_multiplier": rebirth_multiplier,
        "rebirth_count": rebirth_count,
        "items": serializable_items,
        "last_saved_time": time.time()
    }

    with open("save_data.json", "w") as f:
        json.dump(data, f, indent=4)

def load_game(items_template):
    try:
        with open("save_data.json", "r") as f:
            data = json.load(f)

        Knowledge = data.get("Knowledge", 0)
        multiplier = data.get("rebirth_multiplier", 1)
        count = data.get("rebirth_count", 0)
        saved_items = data.get("items", {})
        last_saved_time = data.get("last_saved_time", time.time())

        # Sync saved items into template
        for key in items_template:
            if key in saved_items:
                items_template[key]["owned"] = saved_items[key].get("owned", 0)
                items_template[key]["cost"] = saved_items[key].get("cost", items_template[key]["cost"])

        return Knowledge, multiplier, count, last_saved_time

    except (FileNotFoundError, json.JSONDecodeError):
        return 0, 1, 0, time.time()
