import pandas as pd

# Load data
club_players = pd.read_csv('./data/updated/club_players_updated.csv')

# Calculate average height and mode foot for EVERY unique position
position_stats = club_players.groupby('position').agg({
    'height': 'mean',
    'foot': lambda x: x.mode()[0] if not x.mode().empty else 'right'
}).reset_index()

# Display the calculated averages (optional)
print(position_stats)

"""
# Create mapping dictionaries
height_map = position_stats.set_index('position')['height'].to_dict()
foot_map = position_stats.set_index('position')['foot'].to_dict()

# Fill missing values
club_players['height'] = club_players.apply(
    lambda row: height_map.get(row['position'], club_players['height'].mean())
    if pd.isna(row['height']) else row['height'],
    axis=1
)

club_players['foot'] = club_players.apply(
    lambda row: foot_map.get(row['position'], 'right')
    if pd.isna(row['foot']) else row['foot'],
    axis=1
)

# Round heights to 1 decimal place
club_players['height'] = club_players['height'].round(1)

club_players.to_csv('./data/updated/club_players_updated1.csv', index=False)"""