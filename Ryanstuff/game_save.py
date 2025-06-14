
import time
import json
import os

SAVE_FILE = "save_data.json"

upgrade_defs = [
    {"name": "Book Stand", "base_cost": 10, "base_rate": 0.1, "base_interval": 5.0},
    {"name": "Desk Lamp", "base_cost": 50, "base_rate": 0.5, "base_interval": 4.5},
    {"name": "Whiteboard", "base_cost": 100, "base_rate": 1.0, "base_interval": 4.0},
    {"name": "Encyclopedia Set", "base_cost": 250, "base_rate": 2.0, "base_interval": 3.5},
    {"name": "Research Assistant", "base_cost": 500, "base_rate": 4.0, "base_interval": 3.0},
    {"name": "Study Timer", "base_cost": 750, "base_rate": 6.0, "base_interval": 2.5},
    {"name": "Learning App", "base_cost": 1000, "base_rate": 10.0, "base_interval": 2.0},
    {"name": "Brain Supplements", "base_cost": 1500, "base_rate": 15.0, "base_interval": 1.8},
    {"name": "VR Learning Kit", "base_cost": 2000, "base_rate": 20.0, "base_interval": 1.5},
    {"name": "AI Tutor", "base_cost": 3000, "base_rate": 30.0, "base_interval": 1.2},
]

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

def load_game(upgrade_defs):
    upgrades = []
    knowledge = 0
    multiplier = 1
    rebirth_count = 0
    last_saved_time = time.time()

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)

            knowledge = data.get("Knowledge", 0)
            multiplier = data.get("rebirth_multiplier", 1)
            rebirth_count = data.get("rebirth_count", 0)
            last_saved_time = data.get("last_saved_time", time.time())
            upgrade_levels = data.get("upgrade_levels", [])

            for i, upg_def in enumerate(upgrade_defs):
                level = upgrade_levels[i] if i < len(upgrade_levels) else 0
                upgrades.append({
                    "name": upg_def["name"],
                    "level": level,
                    "last_tick": time.time(),
                    "base_cost": upg_def["base_cost"],
                    "base_rate": upg_def["base_rate"],
                    "base_interval": upg_def["base_interval"],
                    "progress": 0.0,
                    "gif": None,
                    "frames": [],
                    "frame_index": 0
    })


        except Exception as e:
            print("Failed to load save:", e)

    else:
        # No save file - initialize default upgrades
        for upg_def in upgrade_defs:
            upgrades.append({
                "name": upg_def["name"],
                "level": 0,
                "last_tick": time.time()
            })

    return knowledge, upgrades, multiplier, rebirth_count, last_saved_time
