import pandas as pd

# Load the player_market_values file
player_market_values = pd.read_csv('./data/player_market_values.csv')

# Sort the DataFrame by player_id and date to ensure correct order
player_market_values.sort_values(by=['player_id', 'date'], inplace=True)

# Function to fill missing market_value based on the given conditions
def fill_market_value(group):
    # Forward fill (fill missing values with the next row's value)
    group['market_value'] = group['market_value'].ffill()
    
    # Backward fill (fill missing values with the previous row's value)
    group['market_value'] = group['market_value'].bfill()
    
    # Calculate the average of previous and next row for remaining missing values
    for i in range(1, len(group) - 1):
        if pd.isnull(group.iloc[i]['market_value']):
            prev_value = group.iloc[i - 1]['market_value']
            next_value = group.iloc[i + 1]['market_value']
            if not pd.isnull(prev_value) and not pd.isnull(next_value):
                group.at[group.index[i], 'market_value'] = (prev_value + next_value) / 2
    return group

# Apply the function to each player_id group
player_market_values = player_market_values.groupby('player_id').apply(fill_market_value)

# Reset index after groupby operation
player_market_values.reset_index(drop=True, inplace=True)

# Save the updated DataFrame to a new file
player_market_values.to_csv('./data/updated/player_market_values_updated.csv', index=False)

print("Missing values have been filled. Updated data saved to 'player_market_values_updated.csv'.")