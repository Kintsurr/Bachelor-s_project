import pandas as pd

def analyze_missing_values(file_path):
    """
    Reads a CSV file and returns a detailed report of missing values.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    None
    """
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Display basic info
    print(f"Dataset Shape: {df.shape}\n")
    print("First 5 Rows:\n", df.head(), "\n")
    
    # Check for missing values
    missing_counts = df.isnull().sum()
    missing_percentages = (missing_counts / len(df)) * 100
    
    # Combine results
    missing_summary = pd.DataFrame({
        "Missing Values": missing_counts,
        "Percentage (%)": missing_percentages
    })
    
    # Filter only columns with missing values
    missing_summary = missing_summary[missing_summary["Missing Values"] > 0]

    #nationality_missing_rows = df[df["market_value"].isna()]
    #print("\nRows with missing 'nationality':\n", nationality_missing_rows, "\n")

    #print(df[df.isna().any(axis=1)], "\n")
    if missing_summary.empty:
        print("No missing values found in the dataset.")
    else:
        print("Missing Values Report:\n", missing_summary)


def delete_column(file_path, column_name, save_path=None):
    """
    Reads a CSV file, deletes the specified column, and saves the updated file.

    Parameters:
    file_path (str): Path to the input CSV file.
    column_name (str): Name of the column to delete.
    save_path (str, optional): Path to save the updated CSV file. If None, overwrites the original file.

    Returns:
    pd.DataFrame: Updated dataframe without the specified column.
    """
    # Load dataset
    df = pd.read_csv(file_path)

    # Check if the column exists
    if column_name in df.columns:
        df = df.drop(columns=[column_name])
        print(f"Column '{column_name}' deleted successfully.")
    else:
        print(f"Column '{column_name}' not found in the dataset.")

    # Save the updated CSV
    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Updated file saved at: {save_path}")
    else:
        df.to_csv(file_path, index=False)
        print("Original file overwritten with changes.")

    return df

def delete_row_by_id(file_path, id_column, id_value, save_path=None):
    """
    Reads a CSV file, deletes the row(s) where the given ID value matches, and saves the updated file.

    Parameters:
    file_path (str): Path to the input CSV file.
    id_column (str): Name of the ID column.
    id_value: The specific value in the ID column to delete.
    save_path (str, optional): Path to save the updated CSV file. If None, overwrites the original file.

    Returns:
    pd.DataFrame: Updated dataframe without the specified row(s).
    """
    # Load dataset
    df = pd.read_csv(file_path)

    # Check if the column exists
    if id_column in df.columns:
        initial_rows = df.shape[0]
        df = df[df[id_column] != id_value]
        deleted_rows = initial_rows - df.shape[0]

        if deleted_rows > 0:
            print(f"Deleted {deleted_rows} row(s) where {id_column} = {id_value}.")
        else:
            print(f"No rows found with {id_column} = {id_value}.")
    else:
        print(f"Column '{id_column}' not found in the dataset.")

    # Save the updated CSV
    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Updated file saved at: {save_path}")
    else:
        df.to_csv(file_path, index=False)
        print("Original file overwritten with changes.")

    return df

def convert_float_to_int(file_path, column, save_path=None):

    df = pd.read_csv(file_path)
    # Convert the market_value column to integers
    df[column] = df[column].astype(float).astype(int)

    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Updated file saved at: {save_path}")
    else:
        df.to_csv(file_path, index=False)
        print("Original file overwritten with changes.")
    return df
#--------------------------------------------------------

#delete_column("./data/updated/player_transfers_updated.csv", "addressLine2", "./data/updated/player_transfers_updated.csv")
#analyze_missing_values("./data/updated/club_profiles_updated.csv")
#analyze_missing_values("./data/updated/club_players_updated.csv")
#analyze_missing_values("./data/updated/player_injuries_updated.csv")
#analyze_missing_values("./data/updated/player_market_values_updated.csv")
#analyze_missing_values("./data/updated/player_transfer_final1.csv")
#convert_float_to_int("./data/updated/player_market_values_updated.csv", "market_value")
#delete_row_by_id("./data/club_players.csv", "player_id", 1373018)
