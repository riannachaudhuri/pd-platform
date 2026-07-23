import parselmouth
from parselmouth.praat import call
import numpy as np

# =====================================================
# LOAD AUDIO
# =====================================================

audio_file = "audio/1896_ayf_n01.wav"

sound = parselmouth.Sound(audio_file)

# =====================================================
# PITCH FEATURES
# =====================================================

# =====================================================
# PITCH (TUNED SETTINGS)
# =====================================================

pitch = call(
    sound,
    "To Pitch (ac)",
    0.0,     # time step (automatic)
    75,      # pitch floor
    15,      # max number of candidates
    "yes",   # very accurate
    0.03,    # silence threshold
    0.45,    # voicing threshold
    0.01,    # octave cost
    0.35,    # octave-jump cost
    0.14,    # voiced/unvoiced cost
    500      # pitch ceiling
)

pitch_values = pitch.selected_array["frequency"]
pitch_values = pitch_values[pitch_values > 0]

mean_pitch = np.mean(pitch_values)
median_pitch = np.median(pitch_values)
std_pitch = np.std(pitch_values)
min_pitch = np.min(pitch_values)
max_pitch = np.max(pitch_values)

# =====================================================
# INTENSITY
# =====================================================

intensity = sound.to_intensity()
mean_intensity = intensity.values.mean()

# =====================================================
# HNR
# =====================================================

harmonicity = sound.to_harmonicity()
hnr = np.mean(harmonicity.values[harmonicity.values != -200])

# =====================================================
# POINT PROCESS
# =====================================================

point_process = call(
    sound,
    "To PointProcess (periodic, cc)",
    75,
    500
)

# =====================================================
# JITTER
# =====================================================

local_jitter = call(
    point_process,
    "Get jitter (local)",
    0,0,
    0.0001,
    0.02,
    1.3
)

absolute_jitter = call(
    point_process,
    "Get jitter (local, absolute)",
    0,0,
    0.0001,
    0.02,
    1.3
)

rap = call(
    point_process,
    "Get jitter (rap)",
    0,0,
    0.0001,
    0.02,
    1.3
)

ppq5 = call(
    point_process,
    "Get jitter (ppq5)",
    0,0,
    0.0001,
    0.02,
    1.3
)

ddp = 3 * rap

# =====================================================
# SHIMMER
# =====================================================

local_shimmer = call(
    [sound, point_process],
    "Get shimmer (local)",
    0,0,
    0.0001,
    0.02,
    1.3,
    1.6
)

local_shimmer_db = call(
    [sound, point_process],
    "Get shimmer (local_dB)",
    0,0,
    0.0001,
    0.02,
    1.3,
    1.6
)

apq3 = call(
    [sound, point_process],
    "Get shimmer (apq3)",
    0,0,
    0.0001,
    0.02,
    1.3,
    1.6
)

apq5 = call(
    [sound, point_process],
    "Get shimmer (apq5)",
    0,0,
    0.0001,
    0.02,
    1.3,
    1.6
)

apq11 = call(
    [sound, point_process],
    "Get shimmer (apq11)",
    0,0,
    0.0001,
    0.02,
    1.3,
    1.6
)

dda = 3 * apq3

# =====================================================
# FEATURE DICTIONARY
# =====================================================

features = {
    "Mean F0": mean_pitch,
    "Median F0": median_pitch,
    "SD F0": std_pitch,
    "Minimum F0": min_pitch,
    "Maximum F0": max_pitch,

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
}

# =====================================================
# PRINT RESULTS
# =====================================================

print("\n====================================")
print("EXTRACTED FEATURES")
print("====================================")

for feature, value in features.items():
    print(f"{feature:20s}: {value:.6f}")