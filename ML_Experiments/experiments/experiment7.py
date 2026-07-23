import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from sklearn.ensemble import RandomForestClassifier

# ==========================
# Load datasets
# ==========================

italy = pd.read_csv("../data/italy_features_3.csv")
oxford = pd.read_csv("../data/parkinsons.csv")

# Italy labels
italy["Label"] = italy["Label"].map({
    "Healthy": 0,
    "Parkinson": 1
})

# --------------------------
# Matching features
# --------------------------

italy_features = [
    "Mean F0",
    "Max F0",
    "Min F0",
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
    "HNR",
    "RPDE",
    "DFA",
    "Spread1",
    "Spread2",
    "D2",
    "PPE"
]

oxford_features = [
    "MDVP:Fo(Hz)",
    "MDVP:Fhi(Hz)",
    "MDVP:Flo(Hz)",
    "MDVP:Jitter(%)",
    "MDVP:Jitter(Abs)",
    "MDVP:RAP",
    "MDVP:PPQ",
    "Jitter:DDP",
    "MDVP:Shimmer",
    "MDVP:Shimmer(dB)",
    "Shimmer:APQ3",
    "Shimmer:APQ5",
    "MDVP:APQ",
    "Shimmer:DDA",
    "HNR",
    "RPDE",
    "DFA",
    "spread1",
    "spread2",
    "D2",
    "PPE"
]

X_train = italy[italy_features]
X_test = oxford[oxford_features]

# Rename Oxford columns to match Italy columns
X_test.columns = X_train.columns

y_train = italy["Label"]
y_test = oxford["status"]

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(random_state=42))
])

pipeline.fit(X_train, y_train)

pred = pipeline.predict(X_test)
prob = pipeline.predict_proba(X_test)[:,1]

results = pd.DataFrame([{
    "Model":"Random Forest",
    "Accuracy":accuracy_score(y_test,pred),
    "Precision":precision_score(y_test,pred),
    "Recall":recall_score(y_test,pred),
    "F1 Score":f1_score(y_test,pred),
    "ROC AUC":roc_auc_score(y_test,prob)
}])

print(results)

results.to_csv("experiment7_rita.csv",index=False)

print("\nSaved to experiment7_rita.csv")