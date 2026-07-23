import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

# ============================================
# Experiment 5
# Validate Feature Extractor
# Compare Extracted Features vs Human Voices Reference
# ============================================

# Load datasets
reference = pd.read_csv("../data/Speech_dataset_characteristics.csv")
extracted = pd.read_csv("../data/extracted_features.csv")

print("Reference shape:", reference.shape)
print("Extracted shape:", extracted.shape)

# Matching features
feature_map = {
    "Mean F0": "Mean_Pitch(F0)",
    "Median F0": "Median_Pitch(F0)_(Praat_To_Pitch_(ac))",
    "SD F0": "StDev_Pitch(F0)",
    "Min F0": "Pitch_Min_(F0)_(Praat_To_Pitch_(ac))",
    "Max F0": "Pitch_Max_(F0)_(Praat_To_Pitch_(ac))",
    "Mean Intensity": "Mean_Intensity(dB)",
    "HNR": "Harmonics-to-Noise_Ratio",
    "Local Jitter": "Local_Jitter",
    "Absolute Jitter": "Local_Absolute_Jitter",
    "RAP": "RAP_Jitter",
    "PPQ5": "ppq5_Jitter",
    "DDP": "ddp_Jitter",
    "Local Shimmer": "local_shimmer",
    "Local Shimmer dB": "localdb_shimmer",
    "APQ3": "apq3_shimmer",
    "APQ5": "aqpq5_shimmer",
    "APQ11": "apq11_shimmer",
    "DDA": "dda_shimmer",
    "RPDE": "RPDE",
    "DFA": "DFA"
}

results = []

for my_feature, ref_feature in feature_map.items():

    # Skip missing columns
    if my_feature not in extracted.columns:
        print(f"Skipping {my_feature} (not found in extracted features)")
        continue

    if ref_feature not in reference.columns:
        print(f"Skipping {ref_feature} (not found in reference dataset)")
        continue

    # Build temporary dataframe
    temp = pd.DataFrame({
        "Extracted": pd.to_numeric(extracted[my_feature], errors="coerce"),
        "Reference": pd.to_numeric(reference[ref_feature], errors="coerce")
    })

    # Remove missing values
    temp = temp.dropna()

    if len(temp) == 0:
        print(f"No valid values for {my_feature}")
        continue

    x = temp["Extracted"]
    y = temp["Reference"]

    mean_error = np.mean(x - y)
    rmse = np.sqrt(mean_squared_error(y, x))
    correlation = x.corr(y)

    results.append({
        "Feature": my_feature,
        "Mean Error": mean_error,
        "RMSE": rmse,
        "Correlation": correlation
    })

results_df = pd.DataFrame(results)

print("\n===== EXPERIMENT 5 RESULTS =====")
print(results_df)

results_df.to_csv("experiment5_results.csv", index=False)

print("\nResults saved to experiment5_results.csv")