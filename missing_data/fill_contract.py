import pandas as pd
import datetime
# Load data
club_players = pd.read_csv('./data/updated/club_players_updated2.csv')

"""
# Convert to datetime once
club_players['contract'] = pd.to_datetime(club_players['contract'])

# Extract year from existing contracts
contract_years = club_players['contract'].dt.year.dropna()

# Tier 1: Active players (recent transfers)
if 'last_transfer_date' in club_players.columns:
    recent_players = club_players[club_players['last_transfer_date'] > pd.to_datetime('today') - pd.DateOffset(years=2)]
    default_years_recent = round(recent_players['contract'].dt.year.mean())  # e.g., 2026

# Tier 2: Long-term players
else:
    # Base on typical contract lengths by position
    position_contracts = {
        'Goalkeeper': 2,  # Longer contracts for keepers
        'Defender': 1,
        'Midfielder': 1,
        'Forward': 1
    }
    club_players['contract'] = club_players.apply(
        lambda row: pd.to_datetime(f"6/30/{pd.to_datetime('today').year + position_contracts.get(row['position'], 2)}")
        if pd.isna(row['contract']) else row['contract'],
        axis=1
    )

    # Global median of existing contract years (more robust than mean)
median_year = int(contract_years.median()) if not contract_years.empty else datetime.now().year + 2
club_players['contract'] = club_players['contract'].fillna(
    pd.to_datetime(f"6/30/{median_year}")
)
"""

# For joined_on (date column)
club_players['joined_on'] = club_players['joined_on'].fillna('7/1/2024')


# For signed_from (string column)
club_players['signed_from'] = club_players['signed_from'].fillna('Without Club')

club_players.to_csv('./data/updated/club_players_updated3.csv', index=False)
