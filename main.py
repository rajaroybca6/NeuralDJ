import streamlit as st
import streamlit.components.v1 as components
import os
from pathlib import Path
from core.analyzer import get_energy_score, get_transition_point
from core.processor import normalize_tracks

# ==========================================
# 1. AI ANALYSIS & MIXING LOGIC
# ==========================================

# Use ONLY filenames. The modules (analyzer/processor) handle the 'data/' folder logic.
# Ensure these files are pushed to your GitHub repository inside the /data/ folder.
songs = ["test_song.wav", "test2.wav"]

try:
    # AI ranks the 'vibe' - This was line 15 in your error log
    scores = {song: get_energy_score(song) for song in songs}

    # Sort songs: Low energy first -> High energy second
    sorted_songs = sorted(songs, key=lambda x: scores[x])
    song_a_name = sorted_songs[0]
    song_b_name = sorted_songs[1]

    print(f"🎵 AI Decision: Mixing {song_a_name} into {song_b_name}")

    # Proceed with Smart Mixing using filenames
    start_mix_at = get_transition_point(song_a_name)
    song_a, song_b = normalize_tracks(song_a_name, song_b_name)

    # Build and export the AI mix
    final_mix = song_a[:start_mix_at].append(song_b, crossfade=5000)

    # Ensure the export directory exists in the Streamlit environment
    os.makedirs("exports", exist_ok=True)
    final_mix.export("exports/ai_ranked_mix.wav", format="wav")
    print("🔥 AI has built a high-energy transition!")

except FileNotFoundError as e:
    st.error(f"❌ Audio File Error: {e}")
    st.info("Check if your files are in the 'data' folder on GitHub.")
except Exception as e:
    st.error(f"❌ Analysis Error: {e}")

# ==========================================
# 2. STREAMLIT UI & DJ DECK DISPLAY
# ==========================================

st.set_page_config(
    page_title="NeuralDJ ULTRA v2",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Force dark theme style and full-screen for the iframe
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container { padding: 0rem; background-color: #080808; }
        iframe { width: 100vw; height: 1100px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# Path to index.html relative to the project root
html_path = os.path.join("web_app", "templates", "index.html")

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        dj_html = f.read()

    # Render the Deck
    components.html(dj_html, height=1100, scrolling=False)
else:
    st.error(f"❌ Error: index.html not found at {html_path}")

# ==========================================
# 3. FOOTER BRANDING & DOWNLOAD (BELOW DECK)
# ==========================================

st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: white; font-family: sans-serif;'>Created by Raja Roy</h2>",
            unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #E8FF00; font-family: monospace; font-size: 1.2rem;'>⚡ AI ENGINEER</p>",
    unsafe_allow_html=True)

# Centered Download Button
export_path = "exports/ai_ranked_mix.wav"
if os.path.exists(export_path):
    with open(export_path, "rb") as file:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="💾 DOWNLOAD AI-GENERATED MIX",
                data=file,
                file_name="ai_ranked_mix.wav",
                mime="audio/wav",
                use_container_width=True
            )