import json

SAVE_FILE = "save_data.json"

def save_game(Knowledge, player_state, items):
    data = {
        "Knowledge": Knowledge,
        "player_state": player_state,
        "items": items
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        return data["Knowledge"], data["player_state"], data["items"]
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, {"score": 0, "rebirths": 0, "multiplier": 1000.0}, {
            "Cursor": {"cost": 15, "cps": 1, "owned": 0, "progress": 0.0, "speed": 2.0},
            "Grandma": {"cost": 100, "cps": 4, "owned": 0, "progress": 0.0, "speed": 5.0},
        }
