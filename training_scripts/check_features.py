import pandas as pd

# Load the dataset
df = pd.read_csv('./data/merged_features.csv')

# Columns to remove (as per your request)
columns_to_drop = [
    'player_name', 'joined_on', 'signed_from', 'contract',
    'name', 'foundedOn', 'currentTransferRecord',
    'currentMarketValue', 'squad.size', 'squad.averageAge',
    'squad.foreigners', 'squad.nationalTeamPlayers',
    'league.name', 'league.tier'
]

# Remove columns (only those that exist in the DataFrame)
columns_existing = [col for col in columns_to_drop if col in df.columns]
df_clean = df.drop(columns=columns_existing)

# Save the cleaned dataset
df_clean.to_csv('./data/cleaned_features.csv', index=False)

# Verification
print(f"Original columns: {len(df.columns)}")
print(f"Columns removed: {len(columns_existing)}")
print(f"Remaining columns: {len(df_clean.columns)}")
print("\nNew columns:", list(df_clean.columns))