import json
import os

CURRENT_DIR = os.path.dirname(__file__)
PROFILE_DIR = os.path.join(CURRENT_DIR, "profiles")

def save_user_profile(username, age, gender):
    profile = {
        "username": username,
        "age": age,
        "gender": gender
    }
    os.makedirs(PROFILE_DIR, exist_ok=True)
    with open(os.path.join(PROFILE_DIR, f"{username}.json"), "w") as f:
        json.dump(profile, f, indent=4)

def load_user_profile(username):
    profile_path = os.path.join(PROFILE_DIR, f"{username}.json")
    if os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            return json.load(f)
    return None