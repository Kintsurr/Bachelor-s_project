import pandas as pd
import random

# Load all datasets
players = pd.read_csv('./data/club_players_updated.csv')  # Historical values
injury_index = pd.read_csv('./injury_index_calculation/player_injury_indicies.csv')    # From clustering
club_data = pd.read_csv('./data/club_profiles_updated.csv')               # Club performance

# Merge sequentially
df = players.merge(injury_index, on='player_id', how='left') \
                 .merge(club_data, on='club_id', how='left') \

# Handle missing values
df.fillna({
    'injury_index': 2,  # Assume no injuries if missing
     
}, inplace=True)

# Save to file
df.to_csv('./data/merged_features.csv', index=False)