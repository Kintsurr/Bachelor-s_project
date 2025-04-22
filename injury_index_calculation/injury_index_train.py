import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
df = pd.read_csv('./injury_index_calculation/injury_index_features.csv')  # Columns: player_id, injury_rate, missed_days, avg_injury_duration, repeated_injury_rate

# Scale features (critical for clustering)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df.drop('player_id', axis=1))

# Find optimal number of clusters
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    inertia.append(kmeans.inertia_)

# Plot elbow curve
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), inertia, marker='o', linestyle='--')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal K')
plt.savefig('elbow_plot.png')  # Save for documentation
plt.close()

optimal_k = 4  # Change this if you find another number is more optimal

# Fit KMeans with the chosen number of clusters and assign cluster labels
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
df['cluster'] = kmeans.fit_predict(scaled_features)

# Rank clusters from worst (0) to best (100)
cluster_rank = {
    0: 2,   # High-risk cluster
    1: 5,   # Moderate-risk
    2: 7,   # Low-risk
    3: 10   # Minimal/no injuries
}

df['injury_index'] = df['cluster'].map(cluster_rank)

plt.figure(figsize=(12, 8))
sns.scatterplot(
    x='missed_days', 
    y='injury_rate', 
    hue='cluster', 
    palette='viridis', 
    data=df,
    s=100
)
plt.title('Player Injury Clusters')
plt.savefig('injury_clusters.png')
plt.close()

# Save results
df[['player_id', 'injury_index']].to_csv('player_injury_indices.csv', index=False)

# Sample output
print(df[['player_id', 'injury_index']].head())