import joblib
import numpy as np
import parselmouth

# -------------------------
# Load model and scaler
# -------------------------
model = joblib.load("model/pd_model.pkl")
scaler = joblib.load("model/scaler.pkl")

print("Everything loaded successfully!")

# -------------------------
# Load audio
# -------------------------
sound = parselmouth.Sound("audio/hello.wav")

# -------------------------
# Extract features
# -------------------------
pitch = sound.to_pitch()
mean_pitch = pitch.selected_array["frequency"]
mean_pitch = mean_pitch[mean_pitch > 0].mean()

intensity = sound.to_intensity()
mean_intensity = intensity.values.mean()

hnr = sound.to_harmonicity()
mean_hnr = np.mean(hnr.values[hnr.values != -200])

print("\nExtracted Features")
print("------------------")
print("Mean Pitch:", mean_pitch)
print("Mean Intensity:", mean_intensity)
print("Mean HNR:", mean_hnr)

# -------------------------
# Build feature vector
# -------------------------
features = np.zeros((1, 22))

# Fill the features you currently have
features[0, 0] = mean_pitch
features[0, 15] = mean_hnr

# (We'll fill the remaining features later.)

# -------------------------
# Scale features
# -------------------------
features_scaled = scaler.transform(features)

# -------------------------
# Predict
# -------------------------
prediction = model.predict(features_scaled)[0]
probability = model.predict_proba(features_scaled)[0]

print("\nPrediction")
print("-----------")

if prediction == 1:
    print("Parkinson's detected")
else:
    print("Healthy voice")

print(f"Confidence: {max(probability)*100:.2f}%")