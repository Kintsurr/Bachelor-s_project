import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
from xgboost import XGBRegressor

# Load data
df = pd.read_csv('./data/cleaned_features.csv')

# 1. Nationality Preprocessing
df['primary_nationality'] = df['nationality'].str.split(',').str[0].str.strip()

# 2. Feature Engineering
df['position_group'] = df['position'].str.extract('(Forward|Midfield|Back|Goalkeeper)')[0]
df['height_m'] = df['height'] / 100
df['is_multinational'] = df['nationality'].str.contains(',').astype(int)

# 3. Define features and target
X = df.drop(columns=['market_value', 'nationality', 'league.id'])  # addressLine3 seems redundant with club_country
y = df['market_value']

# 4. Column types
numeric_features = ['age', 'height_m', 'injury_index','is_multinational']
categorical_features = ['position_group', 'foot', 'primary_nationality','club_country']

# 5. Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# 6. Models to try
models = {
    'RandomForest': RandomForestRegressor(
        n_estimators=100,
        max_depth=5,        # Prevent overfitting
        min_samples_leaf=10,
        n_jobs=-1,
        random_state=42
    ),
    'XGBoost': XGBRegressor(
        n_estimators=150,
        max_depth=3,
        learning_rate=0.1,
        random_state=42
    )
}

# 7. Train and evaluate
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

results = {}
for name, model in models.items():
    # Create pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', model)
    ])
    
    # Train
    pipeline.fit(X_train, y_train)
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results[name] = {'MAE': mae, 'R2': r2}
    
    # Save model
    joblib.dump(pipeline, f'{name}_pipeline.pkl')
    print(f"{name} trained and saved. MAE: €{mae:,.2f}, R2: {r2:.3f}")

# 8. Feature importance analysis (for best model)
best_model_name = max(results, key=lambda x: results[x]['R2'])
best_pipeline = joblib.load(f'{best_model_name}_pipeline.pkl')

# Get feature names after one-hot encoding
cat_encoder = best_pipeline.named_steps['preprocessor'].named_transformers_['cat']
cat_features = cat_encoder.get_feature_names_out(categorical_features)
all_features = numeric_features + list(cat_features)

# Plot importance (if using tree-based model)
if hasattr(best_pipeline.named_steps['regressor'], 'feature_importances_'):
    importances = best_pipeline.named_steps['regressor'].feature_importances_
    feat_imp = pd.DataFrame({'Feature': all_features, 'Importance': importances})
    feat_imp = feat_imp.sort_values('Importance', ascending=False)
    
    print("\nTop 10 Important Features:")
    print(feat_imp.head(10))