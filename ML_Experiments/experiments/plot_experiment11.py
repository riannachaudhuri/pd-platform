import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

r2ita = pd.read_csv("experiment9_r2ita.csv")
r2oxf = pd.read_csv("experiment10_r2oxf.csv")

metrics = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]

for metric in metrics:

    plt.figure(figsize=(9,5))

    x = np.arange(len(r2ita["Model"]))
    width = 0.35

    plt.bar(x - width/2, r2ita[metric], width, label="R2ita")
    plt.bar(x + width/2, r2oxf[metric], width, label="R2oxf")

    plt.xticks(x, r2ita["Model"], rotation=20)
    plt.ylim(0, 1.05)

    plt.ylabel(metric)
    plt.title(f"Experiment 11 - {metric}: R2ita vs R2oxf")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"experiment11_{metric.replace(' ','_')}.png", dpi=300)
    plt.close()

print("Experiment 11 graphs saved.") 

plt.tight_layout()
plt.savefig(f"experiment11_{metric.replace(' ','_')}.png", dpi=300)
plt.close()

print("Experiment 11 graphs saved.")