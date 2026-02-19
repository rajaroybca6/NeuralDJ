from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from core.analyzer import get_energy_score, get_transition_point, get_bpm
from core.processor import normalize_tracks
import os

def home(request):
    """Displays the upload dashboard and current track list."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data')

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    songs = [f for f in os.listdir(data_path) if f.endswith('.wav')]
    return render(request, 'index.html', {'songs': songs})

def trigger_mix(request):
    """Handles the AI mixing logic and returns JSON for the Live Deck."""
    if request.method == 'POST' and request.FILES.get('song1') and request.FILES.get('song2'):

        # 1. Save uploaded files to the data directory
        fs = FileSystemStorage(location='data')
        file1 = fs.save(request.FILES['song1'].name, request.FILES['song1'])
        file2 = fs.save(request.FILES['song2'].name, request.FILES['song2'])

        path1 = os.path.join('data', file1)
        path2 = os.path.join('data', file2)

        # 2. AI Analysis & Ranking: Determine the higher energy 'banger'
        songs = [path1, path2]
        scores = {song: get_energy_score(song) for song in songs}
        sorted_songs = sorted(songs, key=lambda x: scores[x])

        # 3. Detect BPM & Calculate Fade based on tempo
        bpm = get_bpm(sorted_songs[0])
        fade_ms = 3000 if bpm > 120 else 7000

        # 4. Create the Smart Mix with beat-matched transition
        start_point = get_transition_point(sorted_songs[0])
        s1, s2 = normalize_tracks(sorted_songs[0], sorted_songs[1])
        final_mix = s1[:start_point].append(s2, crossfade=fade_ms)

        # 5. Save the exported mix to a unique path for the history queue
        export_subdir = os.path.join('data', 'exports')
        if not os.path.exists(export_subdir):
            os.makedirs(export_subdir)

        # Optimization: You might want to use a timestamp here so files don't overwrite
        export_filename = "web_result.wav"
        export_path = os.path.join(export_subdir, export_filename)
        final_mix.export(export_path, format="wav")

        # 6. Return JSON data to the frontend for background processing
        return JsonResponse({
            'score1': scores[sorted_songs[0]],
            'score2': scores[sorted_songs[1]],
            'bpm': bpm,
            'fade': fade_ms / 1000,
            'file_url': '/media/exports/web_result.wav',
            'filename': f"Mix_{bpm}BPM.wav" # Essential for the Queue history link
        })

    # Fallback for invalid requests
    return redirect('home')