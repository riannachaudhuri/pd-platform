import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# Load dataset
df = pd.read_csv("../data/parkinsons.csv")

# Create participant IDs from the filename
df["participant"] = df["name"].apply(
    lambda x: "_".join(x.split("_")[1:3])
)

# Get unique participants
participants = df["participant"].unique()

# Lists to store results
accuracies = []
precisions = []
recalls = []
f1_scores = []
auc_scores = []

# Leave-One-Out Cross Validation
for test_participant in participants:

    # Split data
    train_df = df[df["participant"] != test_participant]
    test_df = df[df["participant"] == test_participant]

    # Features and labels
    X_train = train_df.drop(columns=["name", "participant", "status"])
    y_train = train_df["status"]

    X_test = test_df.drop(columns=["name", "participant", "status"])
    y_test = test_df["status"]

    # Scale features
    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate probabilities (needed for ROC AUC)
    probabilities = model.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)

    # ROC AUC only works if both classes exist
    if len(y_test.unique()) == 2:
        auc = roc_auc_score(y_test, probabilities)
    else:
        auc = None

    # Store metrics
    accuracies.append(accuracy)
    precisions.append(precision)
    recalls.append(recall)
    f1_scores.append(f1)
    auc_scores.append(auc)

    # Print results for this participant
    print("\n---------------------------")
    print(f"Participant: {test_participant}")
    print(f"Accuracy : {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall   : {recall:.3f}")
    print(f"F1 Score : {f1:.3f}")

    if auc is not None:
        print(f"ROC AUC  : {auc:.3f}")
    else:
        print("ROC AUC  : N/A (only one class in test set)")

# Calculate average ROC AUC
valid_auc = [x for x in auc_scores if x is not None]

# Print overall results
print("\n==============================")
print("LEAVE-ONE-OUT RESULTS")
print("==============================")
print(f"Average Accuracy : {sum(accuracies)/len(accuracies):.3f}")
print(f"Average Precision: {sum(precisions)/len(precisions):.3f}")
print(f"Average Recall   : {sum(recalls)/len(recalls):.3f}")
print(f"Average F1 Score : {sum(f1_scores)/len(f1_scores):.3f}")

if valid_auc:
    print(f"Average ROC AUC  : {sum(valid_auc)/len(valid_auc):.3f}")
else:
    print("Average ROC AUC  : N/A")