from pydub import AudioSegment
from pathlib import Path

# BASE_DIR finds the root 'NeuralDJ' folder.
# Since this file is in 'core/', we go up two levels (.parent.parent)
BASE_DIR = Path(__file__).resolve().parent.parent

def get_full_path(filename):
    """Helper to join the base directory, data folder, and filename."""
    return str(BASE_DIR / "data" / filename)

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def normalize_tracks(filename_a, filename_b):
    # Convert filenames to absolute paths for the server
    path_a = get_full_path(filename_a)
    path_b = get_full_path(filename_b)

    # Load the files
    song_a = AudioSegment.from_file(path_a)
    song_b = AudioSegment.from_file(path_b)

    # Set standard loudness to -20dB
    target = -20.0
    return match_target_amplitude(song_a, target), match_target_amplitude(song_b, target)