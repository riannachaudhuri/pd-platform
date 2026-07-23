import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("../data/parkinsons.csv")
# Create participant ID
df["participant"] = df["name"].apply(
    lambda x: "_".join(x.split("_")[1:3])
)

print(df[["name", "participant"]].head(20))
print(df["name"].head(20))
print(df.columns.tolist())


# Remove patient name
df = df.drop(columns=["name"])

# Features and labels
X = df.drop(columns=["status", "participant"])
y = df["status"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Normalize the features
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

print("First training sample after scaling:")
print(X_train_scaled[0])
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Create the model
model = RandomForestClassifier(
    random_state=42
)

# Train the model
model.fit(X_train_scaled, y_train)

# Make predictions
predictions = model.predict(X_test_scaled)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)

print("Accuracy:", accuracy)
from sklearn.metrics import confusion_matrix, classification_report, f1_score

# Calculate F1 Score
f1 = f1_score(y_test, predictions)

print("\nF1 Score:", f1)

# Confusion Matrix
cm = confusion_matrix(y_test, predictions)

tn, fp, fn, tp = cm.ravel()

print("\nConfusion Matrix")
print(cm)

print("\nTrue Positives:", tp)
print("True Negatives:", tn)
print("False Positives:", fp)
print("False Negatives:", fn)

# Detailed classification report
print("\nClassification Report")
print(classification_report(y_test, predictions))
print("\n==============================")
print("MODEL EVALUATION")
print("==============================")

print(f"Accuracy: {accuracy:.4f}")
print(f"F1 Score: {f1:.4f}")

print("\nConfusion Matrix")
print(cm)

print(f"\nTrue Positives : {tp}")
print(f"True Negatives : {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")

print("\nLabels")
print("0 = Healthy")
print("1 = Parkinson's")
joblib.dump(model, "../model/pd_model.pkl")
print("Model saved successfully!")

joblib.dump(scaler, "../model/scaler.pkl")
print("Scaler saved successfully!")