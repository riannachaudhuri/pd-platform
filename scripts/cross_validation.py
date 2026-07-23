import pandas as pd

from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("../data/parkinsons.csv")

# Create participant IDs
df["participant"] = df["name"].apply(
    lambda x: "_".join(x.split("_")[1:3])
)

# Features, labels and groups
X = df.drop(columns=["name", "participant", "status"])
y = df["status"]
groups = df["participant"]

# 3-fold Cross Validation
gkf = GroupKFold(n_splits=3)

# -----------------------------
# Models to compare
# -----------------------------
models = {
    "Random Forest": RandomForestClassifier(random_state=42),

    "Support Vector Machine": SVC(
        probability=True,
        random_state=42
    ),

    "K-Nearest Neighbours": KNeighborsClassifier(),

    "Neural Network": MLPClassifier(
        hidden_layer_sizes=(20,),
        max_iter=1000,
        random_state=42
    )
}

results = []

# =====================================================
# Run every model
# =====================================================

for model_name, model in models.items():

    print("\n====================================")
    print(model_name)
    print("====================================")

    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    auc_scores = []

    fold = 1

    for train_index, test_index in gkf.split(X, y, groups):

        X_train = X.iloc[train_index]
        X_test = X.iloc[test_index]

        y_train = y.iloc[train_index]
        y_test = y.iloc[test_index]

        scaler = StandardScaler()

        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, zero_division=0)
        recall = recall_score(y_test, predictions, zero_division=0)
        f1 = f1_score(y_test, predictions, zero_division=0)

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, probabilities)
        else:
            auc = None

        accuracies.append(accuracy)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)

        if auc is not None:
            auc_scores.append(auc)

        print(f"\nFold {fold}")
        print(f"Accuracy : {accuracy:.3f}")
        print(f"Precision: {precision:.3f}")
        print(f"Recall   : {recall:.3f}")
        print(f"F1 Score : {f1:.3f}")

        if auc is not None:
            print(f"ROC AUC  : {auc:.3f}")

        fold += 1

    avg_accuracy = sum(accuracies) / len(accuracies)
    avg_precision = sum(precisions) / len(precisions)
    avg_recall = sum(recalls) / len(recalls)
    avg_f1 = sum(f1_scores) / len(f1_scores)

    if len(auc_scores) > 0:
        avg_auc = sum(auc_scores) / len(auc_scores)
    else:
        avg_auc = None

    results.append([
        model_name,
        avg_accuracy,
        avg_precision,
        avg_recall,
        avg_f1,
        avg_auc
    ])

# =====================================================
# Final Comparison Table
# =====================================================

results_df = pd.DataFrame(
    results,
    columns=[
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC AUC"
    ]
)

print("\n")
print("=" * 60)
print("FINAL MODEL COMPARISON")
print("=" * 60)

print(results_df.round(3))