import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

roxf = pd.read_csv("experiment6_roxf.csv")
rita = pd.read_csv("experiment7_rita.csv")

metrics = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]

for metric in metrics:

    plt.figure(figsize=(9,5))

    x = np.arange(len(roxf["Model"]))
    width = 0.35

    plt.bar(x - width/2, roxf[metric], width, label="Roxf")
    plt.bar(x + width/2, rita[metric], width, label="Rita")

    plt.xticks(x, roxf["Model"], rotation=20)
    plt.ylim(0, 1.05)

    plt.ylabel(metric)
    plt.title(f"Experiment 8 - {metric}: Roxf vs Rita")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"experiment8_{metric.replace(' ','_')}.png", dpi=300)
    plt.close()

print("Experiment 8 graphs saved.")