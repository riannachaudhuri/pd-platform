import pandas as pd

r2ita = pd.read_csv("experiment9_r2ita.csv")
r2oxf = pd.read_csv("experiment10_r2oxf.csv")

best = r2ita.iloc[0]

comparison = pd.DataFrame({
    "Metric": ["Accuracy","Precision","Recall","F1 Score","ROC AUC"],
    "R2ita": [
        best["Accuracy"],
        best["Precision"],
        best["Recall"],
        best["F1 Score"],
        best["ROC AUC"]
    ],
    "R2oxf": [
        r2oxf.loc[0,"Accuracy"],
        r2oxf.loc[0,"Precision"],
        r2oxf.loc[0,"Recall"],
        r2oxf.loc[0,"F1 Score"],
        r2oxf.loc[0,"ROC AUC"]
    ]
})

comparison["Difference"] = comparison["R2ita"] - comparison["R2oxf"]

print(comparison)

comparison.to_csv("experiment11_comparison.csv", index=False)

print("\nSaved to experiment11_comparison.csv")