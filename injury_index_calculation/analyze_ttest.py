import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load data
df_feat = pd.read_csv('./injury_index_calculation/injury_index_features.csv')   # original features
df_idx  = pd.read_csv('player_injury_indices.csv')  # must include 'player_id' and 'cluster'

# 2. Merge on player_id
df = df_idx.merge(df_feat, on='player_id')

# 3. Define features and clusters
features = ['injury_rate', 'missed_days', 'avg_injury_duration', 'repeated_injury_rate']
clusters = sorted(df['injury_index'].unique())

# 4. Compute Welch’s t-tests (one-vs-rest)
results = []
for feature in features:
    for c in clusters:
        group    = df[df['injury_index'] == c][feature]
        others   = df[df['injury_index'] != c][feature]
        t_stat, p_val = ttest_ind(group, others, equal_var=False)
        results.append({
            'feature': feature,
            'injury_index': c,
            't_stat':  t_stat,
            'p_value': p_val
        })

ttest_df = pd.DataFrame(results).sort_values('p_value')
ttest_df.to_csv('ttest_cluster_feature_influence.csv', index=False)

# 5. Print top results
print("\n=== Top feature/cluster differences by significance ===")
print(ttest_df.head(10).to_string(index=False))

# 6. Boxplots for visual inspection
for feature in features:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='injury_index', y=feature, data=df, palette='viridis')
    plt.title(f'Distribution of {feature} by Cluster')
    plt.xlabel('Cluster')
    plt.ylabel(feature)
    plt.tight_layout()
    plt.savefig(f'boxplot_{feature}_by_cluster.png')
    plt.close()
