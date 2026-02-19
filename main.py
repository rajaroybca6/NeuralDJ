import streamlit as st
import streamlit.components.v1 as components
import os
from core.analyzer import get_energy_score, get_transition_point
from core.processor import normalize_tracks

# ==========================================
# 1. AI ANALYSIS & MIXING LOGIC
# ==========================================

# Define song paths
songs = ["data/test_song.wav", "data/test2.wav"]

# AI ranks the 'vibe'
scores = {song: get_energy_score(song) for song in songs}

# Sort songs: Low energy first -> High energy second
sorted_songs = sorted(songs, key=lambda x: scores[x])
song_a_path = sorted_songs[0]
song_b_path = sorted_songs[1]

print(f"🎵 AI Decision: Mixing {song_a_path} (Score: {scores[song_a_path]}) "
      f"into {song_b_path} (Score: {scores[song_b_path]})")

# Proceed with Smart Mixing
start_mix_at = get_transition_point(song_a_path)
song_a, song_b = normalize_tracks(song_a_path, song_b_path)

# Build and export the AI mix
final_mix = song_a[:start_mix_at].append(song_b, crossfade=5000)
os.makedirs("exports", exist_ok=True)
final_mix.export("exports/ai_ranked_mix.wav", format="wav")
print("🔥 AI has built a high-energy transition!")

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

# Load the DJ Deck HTML
html_path = "web_app/templates/index.html"

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

# Horizontal line separator
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)

# Name and Title
st.markdown("<h2 style='text-align: center; color: white; font-family: sans-serif;'>Created by Raja Roy</h2>",
            unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #E8FF00; font-family: monospace; font-size: 1.2rem;'>⚡ AI ENGINEER</p>",
    unsafe_allow_html=True)

# Centered Download Button
if os.path.exists("exports/ai_ranked_mix.wav"):
    with open("exports/ai_ranked_mix.wav", "rb") as file:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="💾 DOWNLOAD AI-GENERATED MIX",
                data=file,
                file_name="ai_ranked_mix.wav",
                mime="audio/wav",
                use_container_width=True
            )