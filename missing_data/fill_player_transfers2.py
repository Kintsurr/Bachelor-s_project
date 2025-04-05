import pandas as pd

# Load the player_transfer file
player_transfer = pd.read_csv('./data/updated/player_transfers_updated.csv')

# Function to fill missing marketValue for a player
def fill_missing_market_value(player_id, df):
    # Get all rows for the player
    player_rows = df[df['player_id'] == player_id]
    
    # Get all unique clubs involved in the player's transfers
    clubs = set(player_rows['clubFrom'].unique()).union(set(player_rows['clubTo'].unique()))
    
    # Find all rows in the DataFrame where any of these clubs are mentioned
    club_rows = df[((df['clubFrom'].isin(clubs)) | (df['clubTo'].isin(clubs))) & (df['marketValue'].notna())]
    
    # Calculate the average marketValue of these rows
    avg_market_value = club_rows['marketValue'].mean()
    
    # Fill the missing marketValue for the player with this average
    df.loc[player_rows.index, 'marketValue'] = df.loc[player_rows.index, 'marketValue'].fillna(avg_market_value)
    
    return df

# Apply the function to fill missing marketValue for all players
for player_id in player_transfer['player_id'].unique():
    player_transfer = fill_missing_market_value(player_id, player_transfer)

# Save the updated DataFrame to a new file
player_transfer.to_csv('./data/updated/player_transfer_final.csv', index=False)

print("Remaining missing values have been filled. Updated data saved to 'player_transfer_final.csv'.")