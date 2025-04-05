import pandas as pd
from datetime import datetime

# Load the player_injuries file
player_injuries = pd.read_csv('./data/player_injuries.csv')

# Convert date columns to datetime
player_injuries['fromDate'] = pd.to_datetime(player_injuries['fromDate'], format='%Y-%m-%d')
player_injuries['untilDate'] = pd.to_datetime(player_injuries['untilDate'], format='%Y-%m-%d', errors='coerce')

# Fill missing untilDate with today's date
today = datetime.today().strftime('%Y-%m-%d')
player_injuries['untilDate'] = player_injuries['untilDate'].fillna(today)

# Convert untilDate back to datetime after filling
player_injuries['untilDate'] = pd.to_datetime(player_injuries['untilDate'], format='%Y-%m-%d')

# Update the days column where untilDate was missing
player_injuries['days'] = (player_injuries['untilDate'] - player_injuries['fromDate']).dt.days + 1

# Save the updated DataFrame to a new file
player_injuries.to_csv('./data/updated/player_injuries_updated.csv', index=False)

print("Missing values have been filled. Updated data saved to 'player_injuries_updated.csv'.")