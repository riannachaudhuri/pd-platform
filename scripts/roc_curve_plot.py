import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import roc_curve, auc

# Load dataset
df = pd.read_csv("../data/parkinsons.csv")

# Participant IDs
df["participant"] = df["name"].apply(
    lambda x: "_".join(x.split("_")[1:3])
)

groups = df["participant"]

X = df.drop(columns=["name", "participant", "status"])
y = df["status"]

gkf = GroupKFold(n_splits=3)

models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "Support Vector Machine": SVC(probability=True, random_state=42),
    "K-Nearest Neighbours": KNeighborsClassifier(),
    "Neural Network": MLPClassifier(
        hidden_layer_sizes=(20,),
        max_iter=1000,
        random_state=42
    )
}

plt.figure(figsize=(8,6))

for name, model in models.items():

    y_true = []
    y_scores = []

    for train_idx, test_idx in gkf.split(X, y, groups):

        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]

        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        scaler = StandardScaler()

        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        model.fit(X_train, y_train)

        probabilities = model.predict_proba(X_test)[:,1]

        y_true.extend(y_test)
        y_scores.extend(probabilities)

    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, label=f"{name} (AUC = {roc_auc:.3f})")

plt.plot([0,1],[0,1],'k--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison of Machine Learning Models for Parkinson's Disease Classification")
plt.legend()

plt.savefig("../model/roc_curves.png")

plt.show()

print("ROC curve saved!")