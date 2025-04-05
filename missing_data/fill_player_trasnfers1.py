import pandas as pd
import numpy as np

# Load the player_transfer and club_players files
player_transfer = pd.read_csv('./data/player_transfers.csv')
club_players = pd.read_csv('./data/updated/club_players_updated.csv')

# Function to fill missing market_value
def fill_market_value(df):
    # Iterate through each player_id group
    for player_id, group in df.groupby('player_id'):
        # Check if all market_value values are missing for this player
        if group['marketValue'].isna().all():
            # Search for market_value in club_players.csv
            club_player_row = club_players[club_players['player_id'] == player_id]
            if not club_player_row.empty:
                market_value = club_player_row['market_value'].values[0]
                df.loc[group.index, 'marketValue'] = market_value
            continue  # Skip to the next player
        
        # If some values are missing, fill them based on the strategy
        group = group.sort_values(by='date', ascending=False)  # Ensure descending order
        market_values = group['marketValue'].values
        
        # Fill missing values in the middle
        for i in range(1, len(market_values) - 1):
            if pd.isna(market_values[i]):
                prev_value = market_values[i - 1]
                next_value = market_values[i + 1]
                if not pd.isna(prev_value) and not pd.isna(next_value):
                    # Fill with the average of previous and next values
                    market_values[i] = (prev_value + next_value) / 2
        
        # Fill missing values at the top (most recent dates)
        for i in range(len(market_values)):
            if pd.isna(market_values[i]):
                if i == 0:  # First row (most recent date)
                    next_value = market_values[i + 1]
                    if not pd.isna(next_value):
                        # If the trend is increasing, increase by 10-15%
                        if i + 1 < len(market_values) and not pd.isna(market_values[i + 1]):
                            trend = market_values[i + 1] - market_values[i + 2] if i + 2 < len(market_values) else 0
                            if trend > 0:  # Increasing trend
                                market_values[i] = next_value * np.random.uniform(1.10, 1.15)
                            elif trend < 0:  # Decreasing trend
                                market_values[i] = next_value * np.random.uniform(0.85, 0.90)
                            else:  # Stable trend
                                market_values[i] = next_value
                else:  # Middle or bottom rows
                    prev_value = market_values[i - 1]
                    if not pd.isna(prev_value):
                        # If the trend is increasing, increase by 10-15%
                        if i - 1 >= 0 and not pd.isna(market_values[i - 1]):
                            trend = market_values[i - 1] - market_values[i - 2] if i - 2 >= 0 else 0
                            if trend > 0:  # Increasing trend
                                market_values[i] = prev_value * np.random.uniform(1.10, 1.15)
                            elif trend < 0:  # Decreasing trend
                                market_values[i] = prev_value * np.random.uniform(0.85, 0.90)
                            else:  # Stable trend
                                market_values[i] = prev_value
        
        # Update the DataFrame with the filled values
        df.loc[group.index, 'marketValue'] = market_values
    
    return df

# Apply the function to fill missing market_value
player_transfer = fill_market_value(player_transfer)

# Save the updated DataFrame to a new file
player_transfer.to_csv('./data/updated/player_transfers_updated.csv', index=False)

print("Missing values have been filled. Updated data saved to 'player_transfer_updated.csv'.")