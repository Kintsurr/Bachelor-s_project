import pandas as pd

# Load the data
player_auc = pd.read_csv('player_auc_values1.csv')  # Contains all calculated AUC values from market_values
club_players = pd.read_csv('./data/club_players_updated.csv')  # Contains additional players with single market_value

# Find player_ids in club_players that aren't in player_auc
missing_players = club_players[~club_players['player_id'].isin(player_auc['player_id'])]

# Calculate rectangle area AUC (market_value * 100) for missing players
missing_players['auc'] = missing_players['market_value'] * 100

# Create the output DataFrames
# 1. AUC values for missing players (same format as player_auc_values.csv)
missing_auc_values = missing_players[['player_id', 'auc']]

# 2. All rows from club_players used in this operation
used_club_players = missing_players.copy()

# Save the files
missing_auc_values.to_csv('missing_players_auc.csv', index=False)
used_club_players.to_csv('used_club_players_records.csv', index=False)

# Print summary
print(f"Found {len(missing_players)} players in club_players not present in market values")
print(f"Created 'missing_players_auc.csv' with calculated AUC values")
print(f"Created 'used_club_players_records.csv' with all source records used")