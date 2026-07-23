from pathlib import Path

from app.audio_processing import trim_silence
from app.audio_validation import validate_audio
import joblib
import pandas as pd

from app.extract_features import extract_features

# ============================================
# Load trained model once when FastAPI starts
# ============================================

model = joblib.load("model/parkinsons_model.pkl")

# ============================================
# Feature order (must match training)
# ============================================

FEATURES = [
    "Mean F0",
    "Median F0",
    "SD F0",
    "Min F0",
    "Max F0",
    "Mean Intensity",
    "HNR",
    "Local Jitter",
    "Absolute Jitter",
    "RAP",
    "PPQ5",
    "DDP",
    "Local Shimmer",
    "Local Shimmer dB",
    "APQ3",
    "APQ5",
    "APQ11",
    "DDA",
    "DFA",
    "RPDE",
    "D2",
    "PPE",
    "Spread1",
    "Spread2"
]

# ============================================
# Predict Parkinson's
# ============================================

def predict_parkinsons(audio_path):

    audio_path = Path(audio_path)

    # ----------------------------------------
    # Trim silence
    # ----------------------------------------

    trimmed_path = audio_path.parent / f"trimmed_{audio_path.name}"

    trim_silence(audio_path, trimmed_path)

    # ----------------------------------------
    # Validate recording
    # ----------------------------------------

    valid, message = validate_audio(trimmed_path)

    if not valid:
        if trimmed_path.exists():
            trimmed_path.unlink()

        return {
            "error": message
        }

    # ----------------------------------------
    # Extract features
    # ----------------------------------------

    feature_dict = extract_features(trimmed_path)

    # Delete temporary trimmed file
    if trimmed_path.exists():
        trimmed_path.unlink()

    # ----------------------------------------
    # Build dataframe
    # ----------------------------------------

    sample = pd.DataFrame([feature_dict])[FEATURES]

    prediction = model.predict(sample)[0]
    probabilities = model.predict_proba(sample)[0]

    if prediction == 1:
        diagnosis = "Parkinson's"
        confidence = probabilities[1]
    else:
        diagnosis = "Healthy"
        confidence = probabilities[0]

    return {
        "diagnosis": diagnosis,
        "confidence": round(confidence * 100, 2),
        "probabilities": {
            "healthy": round(probabilities[0] * 100, 2),
            "parkinsons": round(probabilities[1] * 100, 2)
        },
        "features": feature_dict
    }