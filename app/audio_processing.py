from pathlib import Path

from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def trim_silence(input_path, output_path):
    """
    Removes silence from the beginning and end of an audio recording.

    Parameters
    ----------
    input_path : str | Path
        Original audio file.

    output_path : str | Path
        Path where the trimmed audio will be saved.
    """

    input_path = Path(input_path)
    output_path = Path(output_path)

    # Load audio
    audio = AudioSegment.from_file(input_path)

    # Detect speech regions
    nonsilent = detect_nonsilent(
        audio,
        min_silence_len=200,
        silence_thresh=audio.dBFS - 16
    )

    # If no speech detected, save original
    if len(nonsilent) == 0:
        audio.export(output_path, format="wav")
        return output_path

    # First speech segment
    start = nonsilent[0][0]

    # Last speech segment
    end = nonsilent[-1][1]

    # Keep only speech
    trimmed_audio = audio[start:end]

    # Save trimmed recording
    trimmed_audio.export(output_path, format="wav")

    return output_path