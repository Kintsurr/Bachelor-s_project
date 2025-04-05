import requests
import pandas as pd
import time
import random
from tqdm import tqdm
import os
import concurrent.futures

BASE_URL = "http://localhost:8000"
CLUB_IDS = [0]
#CLUB_IDS = range(1, 4001)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

CSV_FILES = {
    "club_profiles": f"{DATA_DIR}/club_profiles.csv",
    "club_players": f"{DATA_DIR}/club_players1.csv",
    "player_profiles": f"{DATA_DIR}/player_profiles.csv",
    "player_market_values": f"{DATA_DIR}/player_market_values.csv",
    "player_transfers": f"{DATA_DIR}/player_transfers.csv",
    "player_stats": f"{DATA_DIR}/player_stats.csv",
    "player_injuries": f"{DATA_DIR}/player_injuries.csv",
    "player_achievements": f"{DATA_DIR}/player_achievements.csv"
}

ENDPOINTS = {
    "club_profiles": "/clubs/{}/profile",
    "club_players": "/clubs/{}/players",
    "player_profiles": "/players/{}/profile",
    "player_market_values": "/players/{}/market_value",
    "player_transfers": "/players/{}/transfers",
    "player_stats": "/players/{}/stats",
    "player_injuries": "/players/{}/injuries",
    "player_achievements": "/players/{}/achievements"
}


def load_existing_ids(file_path):
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path, usecols=["player_id"])
        return df["player_id"].astype(str).tolist()
    return []


PLAYER_IDS = set(load_existing_ids("./data/club_players.csv"))


SELECTED_COLUMNS = [
    "player_id", "age", "date", "club_id", "marketValue", 
]

def initialize_csv(file_path, columns):
    if not os.path.isfile(file_path):
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

# Function to fetch and save data dynamically
def fetch_data(endpoint, id_list, file_name):
    csv_exists = os.path.isfile(file_name)  # Check if CSV file exists

    for id_value in tqdm(id_list, desc=f"Fetching {file_name}"):
        url = f"{BASE_URL}{endpoint.format(id_value)}"

        try:
            response = requests.get(url, timeout=20)

            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, dict) and data:
                    print(f"✔️ Data for ID {id_value}")  # Debugging output ✅
                    
                    injuries = data["injuries"]
                    value_history_list = []
                    for injury in injuries:
                        player_data = {
                            "player_id": id_value,
                            "season": injury.get("season", ""),
                            "injury": injury.get("injury", ""),
                            "fromDate": injury.get("fromDate", ""),
                            "untilDate": injury.get("untilDate", ""),
                            "days": injury.get("days", "")
                        }
                        value_history_list.append(player_data)
                    
                    df = pd.DataFrame(value_history_list)
                    # ✅ Append data directly to CSV in real-time
                    df.to_csv(file_name, mode='a', header=not csv_exists, index=False)
                    csv_exists = True  # Ensures header is only written once
                else:
                    print(f"⚠️ Skipping ID {id_value} due to missing or invalid data.")

            else:
                print(f"⚠️ Failed to fetch {file_name} for ID {id_value} (Status: {response.status_code})")

        except requests.exceptions.Timeout:
            print(f"⏳ Timeout for {file_name} at ID {id_value}, skipping...")
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection error for {file_name} at ID {id_value}, skipping...")
        except Exception as e:
            print(f"❌ Unexpected error for {file_name} at ID {id_value}: {e}")

        time.sleep(random.uniform(0.5, 3))  # Introduce a small delay


# Fetch all data dynamically
#fetch_data(ENDPOINTS["player_market_values"], CLUB_IDS, CSV_FILES["player_market_values"])
#fetch_data(ENDPOINTS["club_profiles"], CLUB_IDS, CSV_FILES["club_profiles"])
#fetch_data(ENDPOINTS["club_players"], CLUB_IDS, CSV_FILES["club_players"])
#fetch_data(ENDPOINTS["player_transfers"], PLAYER_IDS, CSV_FILES["player_transfers"])
fetch_data(ENDPOINTS["player_injuries"], PLAYER_IDS, CSV_FILES["player_injuries"])
#fetch_data(ENDPOINTS["player_achievements"], PLAYER_IDS, CSV_FILES["player_achievements"])
