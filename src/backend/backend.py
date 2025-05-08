import os
from src import data
import json

# init
if not os.path.exists(data.DATABASE_PATH):
    open(data.DATABASE_PATH, 'w').close()
else:
    with open(data.DATABASE_PATH, 'r') as f:
        data.player_data = json.load(f)


def account_exists(id) -> bool:
    return id in data.player_data.keys()

def get_account_info(id) -> dict:
    return data.player_data[id]

def create_new_player(id, name, birthdate):
    if account_exists(id):
        return # skip if account already exists
    data.player_data[id] = {"name": name, "birthdate": birthdate, "balance": 1000}
    with open(data.DATABASE_PATH, 'w') as f:
        json.dump(data.player_data, f)

def save_current_player():
    if data.current_player_id is not None:
        data.player_data[data.current_player_id] = data.current_player
        with open(data.DATABASE_PATH, 'w') as f:
            json.dump(data.player_data, f)
