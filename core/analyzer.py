import librosa
import numpy as np
from pathlib import Path

# BASE_DIR finds the root 'NeuralDJ' folder.
# Since this file is in 'core/', we go up two levels (.parent.parent)
BASE_DIR = Path(__file__).resolve().parent.parent


def get_full_path(filename):
    """Helper to join the base directory, data folder, and filename."""
    # This ensures the path works on both Windows (local) and Linux (Streamlit)
    return str(BASE_DIR / "data" / filename)


def get_energy_score(file_path):
    """Calculates the 'Hype Factor' of a song."""
    # If file_path is just a name (e.g., 'song.mp3'), convert to absolute path
    full_path = get_full_path(file_path)

    # Load 60 seconds to analyze the 'vibe'
    # Use str() to ensure librosa receives a string path
    y, sr = librosa.load(full_path, duration=60)
    rms = librosa.feature.rms(y=y)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

    # Formula: Combine loudness (RMS) and brightness (Centroid)
    score = (np.mean(rms) * 50) + (np.mean(centroid) / 500)
    return round(float(score), 1)


def get_bpm(file_path):
    """Detects the tempo of the track."""
    full_path = get_full_path(file_path)

    # Load 30s for a quick tempo check
    y, sr = librosa.load(full_path, duration=30)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Librosa returns an array in newer versions; ensure we get a single float/int
    if isinstance(tempo, (np.ndarray, list)):
        tempo = tempo[0]
    return int(tempo)


def get_transition_point(file_path):
    """Finds the perfect beat-synced exit point."""
    full_path = get_full_path(file_path)

    y, sr = librosa.load(full_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # Convert frames to milliseconds for Pydub
    beat_times_ms = librosa.frames_to_time(beat_frames, sr=sr) * 1000

    # Logic: Start the mix exactly 32 beats (8 bars) before the song ends
    if len(beat_times_ms) > 32:
        return int(beat_times_ms[-32])

    # Fallback: if song is too short, return the first beat or 0
    return int(beat_times_ms[0]) if len(beat_times_ms) > 0 else 0