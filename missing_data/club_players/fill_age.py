import pandas as pd
from datetime import datetime, timedelta

# Load the club_players and player_transfers files
club_players = pd.read_csv('./data/club_players.csv')
player_transfers = pd.read_csv('./data/player_transfers.csv')

# Convert date columns to datetime objects
club_players['date_of_birth'] = pd.to_datetime(club_players['date_of_birth'], format='%m/%d/%Y', errors='coerce')
player_transfers['date'] = pd.to_datetime(player_transfers['date'], format='%Y-%m-%d')

# Function to calculate age and date of birth based on the first transfer date
def calculate_age_and_dob(player_id):
    # Filter transfers for the specific player
    player_transfers_filtered = player_transfers[player_transfers['player_id'] == player_id]
    
    if not player_transfers_filtered.empty:
        # Find the earliest transfer date
        first_transfer_date = player_transfers_filtered['date'].min()
        
        # Calculate the number of years since the first transfer
        years_since_first_transfer = (datetime.now() - first_transfer_date).days // 365
        
        # Calculate age (19 + years since first transfer)
        age = 19 + years_since_first_transfer
        
        # Calculate date of birth (current date - age years)
        date_of_birth = datetime.now() - timedelta(days=age*365)
        
        return date_of_birth.strftime('%m/%d/%Y'), age
    else:
        return None, None

# Apply the function to fill missing values in club_players
for index, row in club_players.iterrows():
    if pd.isnull(row['date_of_birth']) or pd.isnull(row['age']):
        player_id = row['player_id']
        date_of_birth, age = calculate_age_and_dob(player_id)
        
        if date_of_birth and age:
            club_players.at[index, 'date_of_birth'] = date_of_birth
            club_players.at[index, 'age'] = age

# Save the updated club_players data to a new file
club_players.to_csv('./data/updated/club_players_updated.csv', index=False)

print("Missing values have been filled and saved to 'club_players_updated.csv'.")