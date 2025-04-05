import pandas as pd
from datetime import datetime
import numpy as np

# Load the club_players file
club_players = pd.read_csv('./data/updated/club_players_updated.csv')

# Convert date_of_birth column to datetime (if not already)
club_players['date_of_birth'] = pd.to_datetime(club_players['date_of_birth'], format='%Y-%m-%d', errors='coerce')

# Calculate the mean age (excluding missing values)
mean_age = int(club_players['age'].mean())

# Function to generate a random date in a specific year
def generate_random_date(year):
    random_month = np.random.randint(1, 13)  # Random month (1-12)
    random_day = np.random.randint(1, 29)    # Random day (1-28 to avoid month-end issues)
    return datetime(year, random_month, random_day).strftime('%Y-%m-%d')

# Fill missing age and date_of_birth columns
for index, row in club_players.iterrows():
    if pd.isnull(row['age']) or pd.isnull(row['date_of_birth']):
        # Fill age with mean age
        club_players.at[index, 'age'] = mean_age
        
        # Calculate birth year based on mean age
        birth_year = datetime.now().year - mean_age
        
        # Generate a random date in the birth year
        random_date = generate_random_date(birth_year)
        club_players.at[index, 'date_of_birth'] = random_date

# Save the updated club_players data to a new file
club_players.to_csv('club_players_updated.csv', index=False)

print(f"Mean age used: {mean_age}")
print("Missing values have been filled. Updated data saved to 'club_players_updated.csv'.")