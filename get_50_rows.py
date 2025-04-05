import pandas as pd

def extract_first_50_rows(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)
    
    # Select the first 50 rows
    first_50_rows = df.head(50)
    
    # Save to a new CSV file
    first_50_rows.to_csv(output_csv, index=False)
    
    print(f"First 50 rows saved to {output_csv}")

# Example usage
input_file = "./data/player_transfers.csv"  # Replace with your actual input file name
output_file = "player_transfers_first_50.csv"  # Replace with your desired output file name
extract_first_50_rows(input_file, output_file)
