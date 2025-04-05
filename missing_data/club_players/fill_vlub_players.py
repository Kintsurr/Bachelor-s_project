import pandas as pd

# Load the club_players file
club_players = pd.read_csv('club_players_updated.csv')

# Fill remaining missing market_value with 25000
club_players['market_value'] = club_players['market_value'].fillna(25000)

# Save the updated DataFrame to a new file
club_players.to_csv('club_players_final.csv', index=False)

print("Remaining missing market_value values have been filled with 25000. Updated data saved to 'club_players_final.csv'.")