import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# ==========================
# Load Italy dataset
# ==========================

italy = pd.read_csv("ML_Experiments/data/italy_features_3.csv")

italy["Label"] = italy["Label"].map({
    "Healthy": 0,
    "Parkinson": 1
})

# ==========================
# Features used by final model
# ==========================

features = [
    "Mean F0",
    "Median F0",
    "SD F0",
    "Min F0",
    "Max F0",
    "Mean Intensity",
    "HNR",
    "Local Jitter",
    "Absolute Jitter",
    "RAP",
    "PPQ5",
    "DDP",
    "Local Shimmer",
    "Local Shimmer dB",
    "APQ3",
    "APQ5",
    "APQ11",
    "DDA",
    "DFA",
    "RPDE",
    "D2",
    "PPE",
    "Spread1",
    "Spread2"
]

X = italy[features]
y = italy["Label"]

# ==========================
# Final Random Forest
# ==========================

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        random_state=42
    ))
])

pipeline.fit(X, y)

joblib.dump(
    pipeline,
    "model/parkinsons_model.pkl"
)

print("✅ Final model saved to model/parkinsons_model.pkl")