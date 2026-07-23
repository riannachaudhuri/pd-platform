import pandas as pd
import numpy as np

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

# ============================================
# Load Oxford Dataset
# ============================================

oxford = pd.read_csv("../data/parkinsons.csv")

print("Oxford dataset shape:", oxford.shape)

print("\nColumns:")
print(oxford.columns.tolist())

print("\nFirst 5 rows:")
print(oxford.head())

# ============================================
# Experiment 2
# Oxford Dataset
# 15 Overlapping Features
# 5-Fold Stratified Cross Validation
# ============================================

features15 = [
    "MDVP:Fo(Hz)",
    "MDVP:Fhi(Hz)",
    "MDVP:Flo(Hz)",
    "HNR",
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
    "Shimmer:DDA"
]

X = oxford[features15]
y = oxford["status"]

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

print("\n===== EXPERIMENT 2 RESULTS =====")
print(results_df)

results_df.to_csv(
    "experiment2_results.csv",
    index=False
)

print("\nResults saved to experiment2_results.csv")