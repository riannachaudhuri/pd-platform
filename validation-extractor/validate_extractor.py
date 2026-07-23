import pandas as pd
import numpy as np

# ======================================================
# LOAD DATA
# ======================================================

published = pd.read_csv("dataset/Speech_dataset_characteristics.csv")
extracted = pd.read_csv("output/extracted_features.csv")

# ======================================================
# MATCH FILES
# ======================================================

published["Audio_Filename"] = (
    published["Audio_Filename"]
    .astype(str)
    .str.replace(".wav", "", regex=False)
)

extracted["Filename"] = (
    extracted["Filename"]
    .astype(str)
    .str.replace(".wav", "", regex=False)
)

merged = pd.merge(
    published,
    extracted,
    left_on="Audio_Filename",
    right_on="Filename"
)

print(f"\nMatched {len(merged)} recordings.\n")

# ======================================================
# FEATURES TO COMPARE
# ======================================================

feature_pairs = {

    "Mean_Pitch(F0)": "Mean F0",
    "Median_Pitch(F0)_(Praat_To_Pitch_(ac))": "Median F0",
    "StDev_Pitch(F0)": "SD F0",
    "Pitch_Min_(F0)_(Praat_To_Pitch_(ac))": "Min F0",
    "Pitch_Max_(F0)_(Praat_To_Pitch_(ac))": "Max F0",

    "Harmonics-to-Noise_Ratio": "HNR",

    "Local_Jitter": "Local Jitter",
    "Local_Absolute_Jitter": "Absolute Jitter",
    "RAP_Jitter": "RAP",
    "ppq5_Jitter": "PPQ5",
    "ddp_Jitter": "DDP",

    "local_shimmer": "Local Shimmer",
    "localdb_shimmer": "Local Shimmer dB",
    "apq3_shimmer": "APQ3",
    "aqpq5_shimmer": "APQ5",
    "apq11_shimmer": "APQ11",
    "dda_shimmer": "DDA",

    "Mean_Intensity(dB)": "Mean Intensity"

}

# ======================================================
# VALIDATION
# ======================================================

results = []

for published_feature, extracted_feature in feature_pairs.items():

    published_values = merged[published_feature]
    extracted_values = merged[extracted_feature]

    diff = published_values - extracted_values

    mae = np.mean(np.abs(diff))
    rmse = np.sqrt(np.mean(diff**2))
    mean_error = np.mean(diff)
    std_error = np.std(diff)
    max_error = np.max(np.abs(diff))

    # Pearson correlation
    correlation = published_values.corr(extracted_values)

    results.append({
        "Feature": extracted_feature,
        "Correlation (r)": correlation,
        "Mean Absolute Error": mae,
        "RMSE": rmse,
        "Mean Error": mean_error,
        "Std Error": std_error,
        "Maximum Error": max_error
    })

results = pd.DataFrame(results)

# Round for readability
results = results.round(6)

print("\n==========================================")
print("FEATURE VALIDATION RESULTS")
print("==========================================")
print(results)

results.to_csv(
    "output/validation_results.csv",
    index=False
)

print("\nValidation report saved to:")
print("output/validation_results.csv")