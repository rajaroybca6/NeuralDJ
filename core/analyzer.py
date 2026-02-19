import librosa
import numpy as np


def get_energy_score(file_path):
    """Calculates the 'Hype Factor' of a song."""
    # Load 60 seconds to analyze the 'vibe'
    y, sr = librosa.load(file_path, duration=60)
    rms = librosa.feature.rms(y=y)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

    # Formula: Combine loudness (RMS) and brightness (Centroid)
    score = (np.mean(rms) * 50) + (np.mean(centroid) / 500)
    return round(float(score), 1)


def get_bpm(file_path):
    """Detects the tempo of the track."""
    # Load 30s for a quick tempo check
    y, sr = librosa.load(file_path, duration=30)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Librosa sometimes returns an array; ensure we get a single integer
    if isinstance(tempo, np.ndarray):
        tempo = tempo[0]
    return int(tempo)


def get_transition_point(file_path):
    """Finds the perfect beat-synced exit point."""
    y, sr = librosa.load(file_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # Convert frames to milliseconds for Pydub
    beat_times_ms = librosa.frames_to_time(beat_frames, sr=sr) * 1000

    # Logic: Start the mix exactly 32 beats (8 bars) before the song ends
    if len(beat_times_ms) > 32:
        return int(beat_times_ms[-32])
    return int(beat_times_ms[0])  # Fallback