import os
from src import data
import json

# init
if not os.path.exists(data.DATABASE_PATH):
    open(data.DATABASE_PATH, 'w').close()
else:
    with open(data.DATABASE_PATH, 'r') as f:
        data.player_data = json.load(f)


def account_exists(hash) -> bool:
    return hash in data.player_data.keys()
