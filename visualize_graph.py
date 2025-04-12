import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV
def visualize_graph(filename, plot_filename, column_name):
    df = pd.read_csv(filename)

    # Check the AUC column name is correctly capitalized
    print(df.columns)

    # Sort by AUC
    df_sorted = df.sort_values(by=column_name)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df_sorted[column_name].values, marker='o', linestyle='-')

    plt.title(f'{column_name}Values in Ascending Order')
    plt.xlabel(f'Player (sorted by {column_name})')
    plt.ylabel(f'{column_name}')  # <-- Use the exact column name!
    plt.grid(True)
    plt.tight_layout()
    #plt.savefig(plot_filename, dpi=100)
    #plt.close()
    plt.show()



visualize_graph('./data/club_players_updated.csv', './players_transfer_values.png', 'market_value')
