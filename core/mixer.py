import os
from pydub import AudioSegment

def blend_songs(song1_filename, song2_filename, output_filename):
    # This finds the 'core' folder where this script lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # This goes up one level to the main 'NeuralDJ' folder
    project_root = os.path.dirname(base_dir)

    # This creates the full 'C:\...\data\test2.wav' path
    path1 = os.path.join(project_root, "data", song1_filename)
    path2 = os.path.join(project_root, "data", song2_filename)
    output_path = os.path.join(project_root, "exports", output_filename)

    print(f"Working on: {path1}")

    # Load the actual audio segments
    song_a = AudioSegment.from_file(path1)
    song_b = AudioSegment.from_file(path2)

    # Blend them
    mixed = song_a.append(song_b, crossfade=5000)

    # Export
    mixed.export(output_path, format="wav")
    print(f"✅ Success! Your first AI mix is here: {output_path}")

if __name__ == "__main__":
    # ONLY use the filenames here, the code above handles the folders!
    blend_songs("test_song.wav", "test2.wav", "my_first_mix.wav")