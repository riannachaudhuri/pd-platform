from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
import shutil
import uuid

from app.predict import predict_parkinsons

app = FastAPI(
    title="Parkinson's Detection API",
    version="1.0"
)

# =====================================================
# Allow Vue Frontend to Connect
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Create uploads folder
# =====================================================

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

# =====================================================
# Home
# =====================================================

@app.get("/")
def home():
    return {
        "message": "Parkinson's Detection API is running!"
    }

# =====================================================
# Health Check
# =====================================================

@app.get("/health")
def health():
    return {
        "status": "OK"
    }

# =====================================================
# Final Prediction Endpoint
# =====================================================

@app.post("/predict")
async def predict(

    ve: UploadFile = File(...),
    vi: UploadFile = File(...),
    vo: UploadFile = File(...),
    vu: UploadFile = File(...),
    d2: UploadFile = File(...)

):

    recordings = [

        ("VE", ve),
        ("VI", vi),
        ("VO", vo),
        ("VU", vu),
        ("D2", d2)

    ]

    # Slightly favour sustained vowels

    weights = {

        "VE": 1.2,
        "VI": 1.2,
        "VO": 1.2,
        "VU": 1.2,
        "D2": 0.8

    }

    healthy_score = 0.0
    parkinsons_score = 0.0

    for phonation, uploaded_file in recordings:

        filename = f"{uuid.uuid4()}.wav"

        save_path = UPLOAD_FOLDER / filename

        try:

            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(uploaded_file.file, buffer)

            # -----------------------------
            # Run prediction safely
            # -----------------------------

            try:

                result = predict_parkinsons(save_path)

            except Exception as e:

                raise HTTPException(
                    status_code=500,
                    detail=f"Prediction failed for {phonation}: {str(e)}"
                )

        finally:

            if save_path.exists():
                save_path.unlink()

        # -----------------------------
        # Validation failed
        # -----------------------------

        if "error" in result:

            raise HTTPException(
                status_code=400,
                detail=f"{phonation}: {result['error']}"
            )

        confidence = result["confidence"] / 100

        weight = weights[phonation]

        if result["diagnosis"] == "Parkinson's":

            parkinsons_score += confidence * weight

        else:

            healthy_score += confidence * weight

    total = healthy_score + parkinsons_score

    if total == 0:

        raise HTTPException(
            status_code=500,
            detail="Unable to compute prediction."
        )

    if parkinsons_score >= healthy_score:

        diagnosis = "Parkinson's"

        confidence = (parkinsons_score / total) * 100

    else:

        diagnosis = "Healthy"

        confidence = (healthy_score / total) * 100

    return {

        "diagnosis": diagnosis,

        "confidence": round(confidence, 2)

    }