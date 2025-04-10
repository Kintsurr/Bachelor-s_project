import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Load the data
df = pd.read_csv('./data/player_market_values_updated.csv')

# Convert date strings to datetime objects
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

# Create directory for saving plots
os.makedirs('player_plots', exist_ok=True)

def plot_and_calculate_auc(player_id, player_df):
    # Get min and max dates for this player
    min_date = player_df['date'].min()
    max_date = player_df['date'].max()
    
 
    # Create 100 equally spaced points in time for this player
    x_axis = pd.date_range(start=min_date, end=max_date, periods=100)
    
    # Convert dates to numeric values for interpolation
    numeric_dates = (player_df['date'] - min_date).dt.days
    numeric_x_axis = (x_axis - min_date).days
    
    # Perform linear interpolation
    interpolated_values = np.interp(numeric_x_axis, 
                                  numeric_dates, 
                                  player_df['market_value'])
    
    # Calculate area under curve
    auc = np.trapz(interpolated_values, dx=1)

    """
       # Create figure
    plt.figure(figsize=(12, 6))
    
    # Plot original data points
    plt.scatter(player_df['date'], player_df['market_value'], 
                color='red', label='Actual Data Points', zorder=3)
    
    # Plot the interpolated curve
    plt.plot(x_axis, interpolated_values, 
             label='Interpolated Curve', linewidth=2, zorder=2)
    
    # Fill under the curve for AUC visualization
    plt.fill_between(x_axis, interpolated_values, alpha=0.2, label='AUC Area')
    
    
    
    # Formatting
    plt.title(f'Player {player_id} Market Value History\n(AUC: {auc:,.2f})')
    plt.xlabel('Date')
    plt.ylabel('Market Value (€)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Format y-axis with Euro symbol and proper scaling
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'€{x:,.0f}'))
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot
    plot_filename = f'player_plots/player_{player_id}_market_value.png'
    plt.savefig(plot_filename, dpi=100)
    plt.close()
    """
    return auc

# Process each player
results = []
for player_id, player_df in df.groupby('player_id'):
    auc = plot_and_calculate_auc(player_id, player_df)
    results.append({'player_id': player_id, 'auc': auc})

# Create results dataframe and save to CSV
results_df = pd.DataFrame(results)
results_df.to_csv('player_auc_values1.csv', index=False)

print("Processing complete!")
print(f"- AUC values saved to 'player_auc_values.csv'")
print(f"- Individual player plots saved to 'player_plots/' directory")
print("\nSample AUC results:")
print(results_df.head())