import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# ROC-AUC Comparison Across Experiments
# ==========================================

experiments = {
    "Exp 1": "experiment1_results.csv",
    "Exp 2": "experiment2_results.csv",
    "Exp 3": "experiment3_results.csv",
    "Exp 4": "experiment4_results.csv",
    "Exp 6": "experiment6_roxf.csv",
    "Exp 7": "experiment7_rita.csv",
    "Exp 9": "experiment9_r2ita.csv",
    "Exp10": "experiment10_r2oxf.csv"
}

summary = []

for exp, file in experiments.items():

    if not os.path.exists(file):
        print(f"{file} not found.")
        continue

    df = pd.read_csv(file)

    best = df.loc[df["ROC AUC"].idxmax()]

    summary.append({
        "Experiment": exp,
        "Model": best["Model"],
        "ROC AUC": best["ROC AUC"]
    })

summary_df = pd.DataFrame(summary)

print(summary_df)

# ==========================================
# Plot
# ==========================================

plt.figure(figsize=(10,6))

bars = plt.bar(
    summary_df["Experiment"],
    summary_df["ROC AUC"]
)

plt.ylim(0,1.05)

plt.ylabel("ROC-AUC")
plt.xlabel("Experiment")
plt.title("Best ROC-AUC Across Experiments")

# Write value + model on bars
for bar, auc, model in zip(
        bars,
        summary_df["ROC AUC"],
        summary_df["Model"]):

    plt.text(
        bar.get_x()+bar.get_width()/2,
        auc+0.015,
        f"{auc:.3f}\n{model}",
        ha="center",
        fontsize=8
    )

plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

plt.savefig("roc_auc_comparison.png", dpi=300)

plt.show()

print("\nSaved as roc_auc_comparison.png")