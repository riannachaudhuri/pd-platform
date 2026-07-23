from pathlib import Path
import parselmouth
from nonlinear_features import extract_dfa

audio_file = next(Path("audio").rglob("*.wav"))

print("Testing:", audio_file)

sound = parselmouth.Sound(str(audio_file))

dfa = extract_dfa(sound)

print("DFA =", dfa)
