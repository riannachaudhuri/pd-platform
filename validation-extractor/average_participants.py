import pandas as pd

# Load extracted features
df = pd.read_csv("output/italy_features.csv")

# Group by participant and label
df_final = (
    df.groupby(["Participant", "Label"], as_index=False)
      .mean(numeric_only=True)
)

print("Original rows:", len(df))
print("Final participants:", len(df_final))

# Save
df_final.to_csv("italy_features_final.csv", index=False)

print("Saved as italy_features_final.csv")