import pandas as pd

years_as_pro = pd.read_csv('./injury_index_calculation/player_years_as_pro.csv')
player_injuries = pd.read_csv('./data/player_injuries_updated.csv')
club_players = pd.read_csv('./data/club_players_updated.csv')


player_ids = player_injuries['player_id'].unique()

def injury_rate(player_df1, player_df2):
    number_of_injuries = len(player_df1)
    if player_df2.empty or player_df2.iloc[0]['years_as_pro'] == 0:
        return 0
    years_as_pro = player_df2.iloc[0]['years_as_pro']
    return number_of_injuries / years_as_pro

def missed_time_rate(player_df1, player_df2):

    total_days = player_df1.iloc[0]['days'].sum()
    years_as_pro = player_df2.iloc[0]['years_as_pro']
    return total_days / years_as_pro

def avg_injury_duration(player_df1,):

    total_days = player_df1.iloc[0]['days'].sum()
    number_of_injuries = len(player_df1)
    return total_days / number_of_injuries

def repeated_injury_rate(player_df1):
    number_of_injuries = len(player_df1)
    df_filtered = player_df1[player_df1['injury'].str.lower() != 'unknown injury']
    if number_of_injuries == 0 or len(df_filtered) == 0:
        return 0
    injury_counts = df_filtered['injury'].value_counts()
    repeated_injuries = injury_counts[injury_counts > 1].index
    repeated_rows = df_filtered[df_filtered['injury'].isin(repeated_injuries)]
    count = len(repeated_rows)
    return count / number_of_injuries


results = []
for player_id in player_ids:
    player_df1 = player_injuries[player_injuries['player_id'] == player_id]
    player_df2 = years_as_pro[years_as_pro['player_id'] == player_id]

    injury_rates = injury_rate(player_df1, player_df2)
    missed_days = missed_time_rate(player_df1, player_df2)
    injury_duration = avg_injury_duration(player_df1)
    repeated_injury_rates = repeated_injury_rate(player_df1)

    results.append({'player_id': player_id, 'injury_rate': injury_rates, 'missed_days': missed_days, "avg_injury_duration": injury_duration, "repeated_injury_rate": repeated_injury_rates})

results_df = pd.DataFrame(results)
results_df=results_df.round(3)
results_df.to_csv('injury_index_features.csv', index=False)
#injury_rate(player_injuries[player_injuries['player_id'] == 3333], years_as_pro[years_as_pro['player_id'] == 3333])
#missed_time_rate(player_injuries[player_injuries['player_id'] == 3333], years_as_pro[years_as_pro['player_id'] == 3333])
