import os
from src import data
import json
from datetime import datetime, timedelta

date_time_format = r"%Y-%m-%d %H:%M:%S"

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

def can_use_daily_bonus(id) -> bool:
    daily_bonus_redeemed = data.player_data[id]["daily_bonus"]
    if daily_bonus_redeemed is None:
        return True
    try:
        input_datetime = datetime.strptime(daily_bonus_redeemed, date_time_format)
        
        # Calculate the time difference
        time_difference = datetime.now() - input_datetime
        
        # Check if the difference is at least 1 day (24 hours)
        return time_difference >= timedelta(days=1)
    
    except ValueError as e:
        # something fishy happened so lets just reset the value
        daily_bonus_redeemed = str(datetime.now())
        return False
    
def daily_bonus_eta(id):
    if data.player_data[id]["daily_bonus"] is None:
        return "You can redeem your daily bonus!"
    try:
        input_datetime = datetime.strptime(data.player_data[id]["daily_bonus"], date_time_format)
        overdue_time = input_datetime + timedelta(days=1)
                    
        time_remaining = overdue_time - datetime.now()
        
        if time_remaining.total_seconds() <= 0:
            return "You can redeem your daily bonus!"
        else:
            total_seconds = int(time_remaining.total_seconds())
            days, remainder = divmod(total_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            parts = []
            if days > 0:
                parts.append(f"{days} day{'s' if days != 1 else ''}")
            if hours > 0:
                parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes > 0:
                parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            if seconds > 0 or not parts:
                parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
                
            status = ", ".join(parts) + " remaining"
        
            return status
    
    except ValueError as e:
        return "Error parsing time: " + str(e)

def create_new_player(id, name, birthdate):
    if account_exists(id):
        return # skip if account already exists
    data.player_data[id] = {"name": name, "birthdate": birthdate, "balance": 1000, "daily_bonus": None}
    with open(data.DATABASE_PATH, 'w') as f:
        json.dump(data.player_data, f)

def save_current_player():
    if data.current_player_id is not None:
        data.player_data[data.current_player_id] = data.current_player
        with open(data.DATABASE_PATH, 'w') as f:
            json.dump(data.player_data, f)
