from pathlib import Path

import parselmouth


def validate_audio(audio_path):
    """
    Validate an uploaded voice recording before prediction.
    Returns:
        (True, "Valid recording")
    or
        (False, "Reason")
    """

    audio_path = Path(audio_path)

    try:
        sound = parselmouth.Sound(str(audio_path))
    except Exception:
        return False, "Unable to read audio file."

    duration = sound.get_total_duration()

    # -----------------------------------
    # Duration Check
    # -----------------------------------

    if duration < 4:
        return False, (
            "Recording is too short. "
            "Please sustain the vowel 'A' for at least 5 seconds."
        )

    if duration > 8:
        return False, (
            "Recording is too long. "
            "Please keep the recording between 5 and 6 seconds."
        )

    # -----------------------------------
    # Voice Detection
    # -----------------------------------

    pitch = sound.to_pitch()

    voiced = pitch.selected_array["frequency"]
    voiced = voiced[voiced > 0]

    if len(voiced) == 0:
        return False, (
            "No clear voice detected. Please try again."
        )

    # -----------------------------------
    # Success
    # -----------------------------------

    return True, "Valid recording"