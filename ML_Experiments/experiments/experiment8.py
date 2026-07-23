import pandas as pd

roxf = pd.read_csv("experiment6_roxf.csv")
rita = pd.read_csv("experiment7_rita.csv")

# Best Oxford baseline model
best_roxf = roxf.iloc[0]

comparison = pd.DataFrame({
    "Metric": ["Accuracy","Precision","Recall","F1 Score","ROC AUC"],
    "Roxf": [
        best_roxf["Accuracy"],
        best_roxf["Precision"],
        best_roxf["Recall"],
        best_roxf["F1 Score"],
        best_roxf["ROC AUC"]
    ],
    "Rita": [
        rita.loc[0,"Accuracy"],
        rita.loc[0,"Precision"],
        rita.loc[0,"Recall"],
        rita.loc[0,"F1 Score"],
        rita.loc[0,"ROC AUC"]
    ]
})

comparison["Difference"] = comparison["Roxf"] - comparison["Rita"]

print("\n===== EXPERIMENT 8 =====")
print(comparison)

comparison.to_csv("experiment8_comparison.csv", index=False)

print("\nSaved to experiment8_comparison.csv")