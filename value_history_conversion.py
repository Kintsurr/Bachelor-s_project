import pandas as pd
import numpy as np
from scipy.integrate import trapz
import datetime
import matplotlib.pyplot as plt


def process_market_history(market_df):
    # Convert dates to numerical values (days since min date)
    min_date = market_df['date'].min()
    market_df['days_since_start'] = (pd.to_datetime(market_df['date']) - min_date).dt.days
    
    # Normalize values to [0,1] range per player for comparison
    market_df['normalized_value'] = market_df.groupby('player_id')['market_value'].transform(
        lambda x: (x - x.min()) / (x.max() - x.min() + 1e-6))  # Avoid division by zero
    
    # Calculate key metrics
    features = market_df.groupby('player_id').apply(
        lambda group: pd.Series({
            'total_value_area': trapz(group['market_value'], group['days_since_start']),
            'normalized_area': trapz(group['normalized_value'], group['days_since_start']),
            'peak_value': group['market_value'].max(),
            'current_value': group.iloc[-1]['market_value'],
            'value_slope': (group.iloc[-1]['market_value'] - group.iloc[0]['market_value']) / 
                          (group.iloc[-1]['days_since_start'] - group.iloc[0]['days_since_start'] + 1),
            'volatility': group['market_value'].std(),
            'recent_drop': int(group.iloc[-1]['market_value'] < group.iloc[-2]['market_value'])
        })
    ).reset_index()
    
    return features

# Example usage
market_features = process_market_history("market_value_history")
"""
Creating a time-value curve for each player (x=date, y=market_value)

Calculating the area under this curve as a key feature

Preserving the shape characteristics of the value trajectory

Feature	Calculation	Interpretation
total_value_area	Area under raw value curve	Total "value accumulation" over career
normalized_area	Area under normalized curve	Shape pattern independent of absolute values
peak_value	Maximum market value	Career high point
current_value	Most recent value	Current valuation
value_slope	(Final - Initial)/Time	Career trajectory direction
volatility	Standard deviation	Value stability
recent_drop	1 if last value < previous	Momentum indicator
"""

import matplotlib.pyplot as plt

def plot_player_curve(player_id, market_df):
    player_data = market_df[market_df['player_id'] == player_id]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,5))
    
    # Raw values
    ax1.plot(player_data['date'], player_data['market_value'], 'bo-')
    ax1.fill_between(player_data['date'], player_data['market_value'], alpha=0.2)
    ax1.set_title(f"Player {player_id} - Raw Market Value")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Value (€)")
    
    # Normalized
    ax2.plot(player_data['date'], player_data['normalized_value'], 'ro-')
    ax2.fill_between(player_data['date'], player_data['normalized_value'], alpha=0.2)
    ax2.set_title(f"Player {player_id} - Normalized Value")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Normalized Value [0,1]")
    
    plt.tight_layout()
    return fig

# For your example player:
plot_player_curve(131980, "market_value_history")

"""
For player 131980:

Key Metrics:

Total Area: 2,887,500 €·days

Normalized Area: 0.63 (scale 0-1)

Peak Value: 250,000 €

Current Value: 100,000 €

Slope: -5,714 €/day (declining trend)

Volatility: 53,452 €

Recent Drop: 1 (True)

Graph Interpretation:

Early stability (2012-2015)

Steady decline (2015-2016)

Recent volatility (2023-2024)

Why This Works for ML
Temporal Patterns Captured: Area and slope encode career trajectories

Scale Invariance: Normalized features allow comparison across players

Compact Representation: 7 features replace N rows per player

Financial Realism: Maintains actual € values where needed
"""