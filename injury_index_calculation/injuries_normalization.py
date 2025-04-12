import pandas as pd

# Load the cleaned injury data
df = pd.read_csv('./data/player_injuries_updated.csv')

# Get unique injury types (case-insensitive, trimmed)
injury_types = (df['injury']
                .unique()     # Get unique values
                .tolist()     # Convert to list
               )

# Sort alphabetically
injury_types_sorted = sorted(injury_types)

# Print for review
print(f"Found {len(injury_types_sorted)} unique injury types:")
for injury in injury_types_sorted:
    print(f"- {injury.title()}")  # Title case for readability

injury_weights_df = pd.DataFrame({
    'injury_type': injury_types_sorted,
    'severity_weight': None  # To be filled manually
})

injury_weights_df.to_csv('injury_severity_weights_template.csv', index=False)
print("\nTemplate saved to 'injury_severity_weights_template.csv'")