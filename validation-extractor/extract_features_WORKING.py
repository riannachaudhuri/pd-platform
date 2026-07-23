import parselmouth
from parselmouth.praat import call
import numpy as np
import pandas as pd
from pathlib import Path

# =====================================================
# FIND ALL WAV FILES
# =====================================================

audio_folder = Path("audio")

audio_files = sorted(audio_folder.rglob("*.wav"))

print(f"\nFound {len(audio_files)} audio files.\n")

results = []

# =====================================================
# PROCESS EACH FILE
# =====================================================

for audio_file in audio_files:

    print(f"Processing: {audio_file.name}")

    try:

        # IMPORTANT: convert Path -> string
        sound = parselmouth.Sound(str(audio_file))

        # ---------------- Pitch ----------------

        pitch = sound.to_pitch()

        pitch_values = pitch.selected_array["frequency"]
        pitch_values = pitch_values[pitch_values != 0]

        if len(pitch_values) == 0:
            print("Skipped (no voiced frames)")
            continue

        mean_pitch = np.mean(pitch_values)
        median_pitch = np.median(pitch_values)
        std_pitch = np.std(pitch_values)
        min_pitch = np.min(pitch_values)
        max_pitch = np.max(pitch_values)

        # ---------------- Intensity ----------------

        intensity = sound.to_intensity()
        mean_intensity = intensity.values.mean()

        # ---------------- HNR ----------------

        harmonicity = sound.to_harmonicity()
        hnr = np.mean(harmonicity.values[harmonicity.values != -200])

        # ---------------- Point Process ----------------

        point_process = call(
            sound,
            "To PointProcess (periodic, cc)",
            75,
            500
        )

        # ---------------- Jitter ----------------

        local_jitter = call(
            point_process,
            "Get jitter (local)",
            0, 0,
            0.0001,
            0.02,
            1.3
        )

        absolute_jitter = call(
            point_process,
            "Get jitter (local, absolute)",
            0, 0,
            0.0001,
            0.02,
            1.3
        )

        rap = call(
            point_process,
            "Get jitter (rap)",
            0, 0,
            0.0001,
            0.02,
            1.3
        )

        ppq5 = call(
            point_process,
            "Get jitter (ppq5)",
            0, 0,
            0.0001,
            0.02,
            1.3
        )

        ddp = 3 * rap

        # ---------------- Shimmer ----------------

        local_shimmer = call(
            [sound, point_process],
            "Get shimmer (local)",
            0, 0,
            0.0001,
            0.02,
            1.3,
            1.6
        )

        local_shimmer_db = call(
            [sound, point_process],
            "Get shimmer (local_dB)",
            0, 0,
            0.0001,
            0.02,
            1.3,
            1.6
        )

        apq3 = call(
            [sound, point_process],
            "Get shimmer (apq3)",
            0, 0,
            0.0001,
            0.02,
            1.3,
            1.6
        )

        apq5 = call(
            [sound, point_process],
            "Get shimmer (apq5)",
            0, 0,
            0.0001,
            0.02,
            1.3,
            1.6
        )

        apq11 = call(
            [sound, point_process],
            "Get shimmer (apq11)",
            0, 0,
            0.0001,
            0.02,
            1.3,
            1.6
        )

        dda = 3 * apq3

        # ---------------- Save ----------------

        results.append({

            "Filename": audio_file.name,

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
            "DDA": dda
        })

    except Exception as e:
        print(f"Skipped {audio_file.name}: {e}")

# =====================================================
# SAVE CSV
# =====================================================

df = pd.DataFrame(results)

output_folder = Path("output")
output_folder.mkdir(exist_ok=True)

output_file = output_folder / "extracted_features.csv"

df.to_csv(output_file, index=False)

print("\n======================================")
print("FEATURE EXTRACTION COMPLETE")
print("======================================")
print(f"Processed {len(df)} audio files.")
print(f"Results saved to:\n{output_file}")
print("======================================")