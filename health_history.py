import json
import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
HISTORY_DIR = os.path.join(CURRENT_DIR, "profiles")

def save_health_history(username, symptoms, results):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "symptoms": symptoms,
        "diagnosis": results
    }

    history_file = os.path.join(HISTORY_DIR, f"{username}_history.json")
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)

    history.append(entry)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)

def load_health_history(username):
    history_file = os.path.join(HISTORY_DIR, f"{username}_history.json")
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return json.load(f)
    return []