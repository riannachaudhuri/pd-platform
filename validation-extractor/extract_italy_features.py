import parselmouth
from parselmouth.praat import call

import numpy as np
import pandas as pd
import gc

from pathlib import Path

from app.nonlinear_features import (
    extract_dfa,
    extract_rpde,
    extract_d2,
    extract_ppe,
    extract_spread1,
    extract_spread2
)


# =====================================================
# ITALIAN DATASET LOCATION
# =====================================================

DATASET_ROOT = Path("italy_dataset")

OUTPUT_FOLDER = Path("output")
OUTPUT_FOLDER.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_FOLDER / "italy_features.csv"


# =====================================================
# FEATURE EXTRACTION FOR ONE AUDIO FILE
# =====================================================

def extract_features(sound):

    # ---------- Nonlinear ----------

    dfa = extract_dfa(sound)

    rpde = extract_rpde(sound)


    d2 = extract_d2(sound)
   

    ppe = extract_ppe(sound)
    

    spread1 = extract_spread1(sound)
    

    spread2 = extract_spread2(sound)
    
    # ---------- Pitch ----------

    pitch = sound.to_pitch()

    pitch_values = pitch.selected_array["frequency"]
    pitch_values = pitch_values[pitch_values != 0]

    if len(pitch_values) == 0:
        return None

    mean_pitch = np.mean(pitch_values)
    median_pitch = np.median(pitch_values)
    std_pitch = np.std(pitch_values)
    min_pitch = np.min(pitch_values)
    max_pitch = np.max(pitch_values)

    # ---------- Intensity ----------

    intensity = sound.to_intensity()
    mean_intensity = intensity.values.mean()

    # ---------- Harmonicity ----------

    harmonicity = sound.to_harmonicity()

    hnr = np.mean(
        harmonicity.values[
            harmonicity.values != -200
        ]
    )

    # ---------- Point Process ----------

    point_process = call(
        sound,
        "To PointProcess (periodic, cc)",
        75,
        500
    )

    # ---------- Jitter ----------

    local_jitter = call(
        point_process,
        "Get jitter (local)",
        0,
        0,
        0.0001,
        0.02,
        1.3
    )

    absolute_jitter = call(
        point_process,
        "Get jitter (local, absolute)",
        0,
        0,
        0.0001,
        0.02,
        1.3
    )

    rap = call(
        point_process,
        "Get jitter (rap)",
        0,
        0,
        0.0001,
        0.02,
        1.3
    )

    ppq5 = call(
        point_process,
        "Get jitter (ppq5)",
        0,
        0,
        0.0001,
        0.02,
        1.3
    )

    ddp = 3 * rap

    # ---------- Shimmer ----------

    local_shimmer = call(
        [sound, point_process],
        "Get shimmer (local)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6
    )

    local_shimmer_db = call(
        [sound, point_process],
        "Get shimmer (local_dB)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6
    )

    apq3 = call(
        [sound, point_process],
        "Get shimmer (apq3)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6
    )

    apq5 = call(
        [sound, point_process],
        "Get shimmer (apq5)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6
    )

    apq11 = call(
        [sound, point_process],
        "Get shimmer (apq11)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6
    )

    dda = 3 * apq3

    return {

        "Mean F0": mean_pitch,
        "Median F0": median_pitch,
        "SD F0": std_pitch,
        "Min F0": min_pitch,
        "Max F0": max_pitch,

        "Mean Intensity": mean_intensity,

        "HNR": hnr,

        "Local Jitter": local_jitter,
        "Absolute Jitter": absolute_jitter,
        "RAP": rap,
        "PPQ5": ppq5,
        "DDP": ddp,

        "Local Shimmer": local_shimmer,
        "Local Shimmer dB": local_shimmer_db,
        "APQ3": apq3,
        "APQ5": apq5,
        "APQ11": apq11,
        "DDA": dda,

        "DFA": dfa,
        
        "RPDE": rpde,

        "D2": d2,

        "PPE": ppe,

        "Spread1": spread1,

        "Spread2": spread2

     }
# =====================================================
# PROCESS ONE PARTICIPANT
# =====================================================

def process_participant(participant_folder, label):

    print(f"\nProcessing participant: {participant_folder.name}")

    wav_files = sorted(participant_folder.glob("*.wav"))

    if len(wav_files) == 0:
        print("No wav files found.")
        return None

    participant_features = []

    for wav in wav_files:
        if participant_folder.name == "LUIGI P":
         print("Testing:", wav.name)

        try:

            print(f"   {wav.name}")

            sound = parselmouth.Sound(str(wav))

            features = extract_features(sound)
            if participant_folder.name == "LUIGI P":
             print(features is None)

            if features is not None:
                participant_features.append(features)

        except Exception as e:

            print(f"      Skipped: {e}")

    if len(participant_features) == 0:
     print(f"No valid features extracted for {participant_folder.name}")
     return None

    df = pd.DataFrame(participant_features)

    mean_features = df.mean(numeric_only=True)

    result = {

        "Participant": participant_folder.name,
        "Label": label

    }

    result.update(mean_features.to_dict())

    return result


