import pandas as pd
import numpy as np

# Load Italy dataset
italy = pd.read_csv("../data/italy_features_3.csv")

# Display basic information
print("Italy dataset shape:", italy.shape)
print("\nColumns:")
print(italy.columns.tolist())

print("\nFirst 5 rows:")
print(italy.head())

from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# -----------------------------
# Experiment 1 - Italy (15 overlapping features)
# -----------------------------

from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# Convert labels to binary
print(italy["Label"].unique())

# ============================================
# Experiment 1
# Italy Dataset
# 18 Overlapping Features
# 5-Fold Stratified Cross Validation
# ============================================

# Convert labels to binary
italy["Label"] = italy["Label"].map({
    "Healthy": 0,
    "Parkinson": 1
})

# 18 overlapping features
features18 = [
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
    "DDA"
]

X = italy[features18]
y = italy["Label"]

# Models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": SVC(probability=True),
    "Random Forest": RandomForestClassifier(random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "KNN": KNeighborsClassifier(),
    "Naive Bayes": GaussianNB()
}

skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

results = []

for name, model in models.items():

    accuracy = []
    precision = []
    recall = []
    f1 = []
    roc_auc = []

    for train_index, test_index in skf.split(X, y):

        X_train = X.iloc[train_index]
        X_test = X.iloc[test_index]

        y_train = y.iloc[train_index]
        y_test = y.iloc[test_index]

        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", model)
        ])

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        if hasattr(pipeline, "predict_proba"):
            probabilities = pipeline.predict_proba(X_test)[:, 1]
        else:
            probabilities = pipeline.decision_function(X_test)

        accuracy.append(accuracy_score(y_test, predictions))
        precision.append(precision_score(y_test, predictions))
        recall.append(recall_score(y_test, predictions))
        f1.append(f1_score(y_test, predictions))
        roc_auc.append(roc_auc_score(y_test, probabilities))

    results.append({
        "Model": name,
        "Accuracy": np.mean(accuracy),
        "Precision": np.mean(precision),
        "Recall": np.mean(recall),
        "F1 Score": np.mean(f1),
        "ROC AUC": np.mean(roc_auc)
    })

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="ROC AUC",
    ascending=False
)

print("\n===== EXPERIMENT 1 RESULTS =====")
print(results_df)

# Save results
results_df.to_csv(
    "experiment1_results.csv",
    index=False
)

print("\nResults saved to results/experiment1_results.csv")