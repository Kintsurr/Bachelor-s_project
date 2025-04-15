import pandas as pd
import numpy as np



# Load the data
player_market_valeus = pd.read_csv('./data/player_market_values_updated.csv')  # Contains all calculated AUC values from market_values
club_players = pd.read_csv('./data/club_players_updated.csv')  # Contains additional players with single market_value


values1 = player_market_valeus['player_id'].unique()
club_players1 = club_players['player_id'].unique()
missing_ids = list(np.setdiff1d(club_players1, values1))


def calculate_years_as_pro(player_id, player_df1, player_df2):
   
    min_age = player_df1['age'].min()
    current_age = int(player_df2['age'])
    years_as_pro =current_age - min_age
    if years_as_pro < 1:
        years_as_pro = 1
    return years_as_pro

def calculate_years_as_pro_missing(player_df):
   
    min_age = 18
    current_age = int(player_df['age'])
    years_as_pro =current_age - min_age
    if years_as_pro < 1:
        years_as_pro = 1
    return years_as_pro

results = []
"""
for player_id, player_df1 in player_market_valeus.groupby('player_id'):
    player_df2 = club_players[club_players['player_id'] == player_id]
    years_as_pro = calculate_years_as_pro(player_id, player_df1, player_df2)
    results.append({'player_id': player_id, 'years_as_pro': years_as_pro})
"""
for player_id in missing_ids:
    club_players_missing = club_players[club_players['player_id'] == player_id]
    years_as_pro = calculate_years_as_pro_missing(club_players_missing)
    results.append({'player_id': player_id, 'years_as_pro': years_as_pro})

results_df = pd.DataFrame(results)
results_df.to_csv('player_years_as_pro1.csv', index=False)