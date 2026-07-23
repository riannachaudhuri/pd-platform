from pathlib import Path
import parselmouth

from nonlinear_features import extract_dfa
from nonlinear_features import extract_rpde

audio_file = next(Path("audio").rglob("*.wav"))

print("Testing:", audio_file)

sound = parselmouth.Sound(str(audio_file))

print("DFA :", extract_dfa(sound))
print("RPDE:", extract_rpde(sound))