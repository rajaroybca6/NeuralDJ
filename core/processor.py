from pydub import AudioSegment


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def normalize_tracks(path_a, path_b):
    song_a = AudioSegment.from_file(path_a)
    song_b = AudioSegment.from_file(path_b)

    # Set standard loudness to -20dB
    target = -20.0
    return match_target_amplitude(song_a, target), match_target_amplitude(song_b, target)