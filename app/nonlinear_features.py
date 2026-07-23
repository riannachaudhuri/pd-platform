import numpy as np
import nolds
from pyrpde import rpde


# =====================================================
# Detrended Fluctuation Analysis (DFA)
# =====================================================

def extract_dfa(sound):

    signal = sound.values.flatten()
    signal = signal - np.mean(signal)

    # Downsample to reduce memory
    signal = signal[::8]

    try:
        return float(nolds.dfa(signal))
    except Exception:
        return np.nan


# =====================================================
# RPDE
# =====================================================

def extract_rpde(sound):

    signal = sound.values.flatten()
    signal = signal - np.mean(signal)
    signal = signal / np.max(np.abs(signal))

    # Even more aggressive downsampling
    signal = signal[::128]

    signal = signal.astype(np.float32)

    try:
        value, _ = rpde(signal)
        return float(value)
    except Exception:
        return np.nan


# =====================================================
# D2
# =====================================================

def extract_d2(sound):

    signal = sound.values.flatten()
    signal = signal - np.mean(signal)
    signal = signal / np.max(np.abs(signal))

    # This is the biggest memory saver
    signal = signal[::256]

    try:
        return float(
            nolds.corr_dim(
                signal,
                emb_dim=2
            )
        )
    except Exception:
        return np.nan


# =====================================================
# PPE
# =====================================================

def extract_ppe(sound):

    signal = sound.values.flatten()
    signal = signal - np.mean(signal)
    signal = signal / np.max(np.abs(signal))

    periods = 1 / (np.abs(signal) + 1e-8)

    hist, _ = np.histogram(
        periods,
        bins=50,
        density=True
    )

    hist = hist[hist > 0]

    return float(-np.sum(hist * np.log2(hist)))


# =====================================================
# Spread1
# =====================================================

def extract_spread1(sound):

    signal = sound.values.flatten()
    signal = signal - np.mean(signal)
    signal = signal / np.max(np.abs(signal))

    diff = np.diff(signal)

    return float(np.std(diff))


# =====================================================
# Spread2
# =====================================================

def extract_spread2(sound):

    signal = sound.values.flatten()
    signal = signal - np.mean(signal)
    signal = signal / np.max(np.abs(signal))

    diff = np.diff(signal)

    mean_diff = np.mean(diff)
    std_diff = np.std(diff)

    return float(np.sqrt(mean_diff**2 + std_diff**2))