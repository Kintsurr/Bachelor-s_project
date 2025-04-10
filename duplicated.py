import pandas as pd

# Load the club_players data
club_players = pd.read_csv('player_auc_values1.csv')

total_rows_before = len(club_players)
duplicate_count = club_players.duplicated(subset=['player_id'], keep=False).sum()
unique_players_before = club_players['player_id'].nunique()

print(f"Before cleaning:")
print(f"- Total rows: {total_rows_before}")
print(f"- Duplicate rows: {duplicate_count}")
print(f"- Unique players: {unique_players_before}")

"""
# Remove duplicates (keeping first occurrence)
club_players_clean = club_players.drop_duplicates(subset=['player_id'], keep='first')

# Count after cleaning
total_rows_after = len(club_players_clean)
unique_players_after = club_players_clean['player_id'].nunique()

print(f"\nAfter cleaning:")
print(f"- Total rows: {total_rows_after}")
print(f"- Rows removed: {total_rows_before - total_rows_after}")
print(f"- Unique players: {unique_players_after}")

# Verify no duplicates remain
assert club_players_clean['player_id'].duplicated().sum() == 0, "Duplicates still exist!"

# Save back to the original file (overwrite)
club_players_clean.to_csv('./data/club_players_updated.csv', index=False)

print("\nDuplicate removal complete. File saved back to club_players.csv")"""