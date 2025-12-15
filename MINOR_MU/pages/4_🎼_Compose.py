import streamlit as st
from gen.compose import compose_song_wav

st.title("🎼 Composer (Chords + Melody + Instrumentation)")

# Sliders for BPM and Bars
bpm = st.slider("BPM", 60, 150, 100)
bars = st.slider("Bars", 4, 32, 8)

# All 72 keys (12 roots × 6 scales)
keys = [
    # Major scales
    "C", "C major", "C minor", "C natural minor", "C harmonic minor", "C melodic minor",
    "C#", "C# major", "C# minor", "C# natural minor", "C# harmonic minor", "C# melodic minor",
    "D", "D major", "D minor", "D natural minor", "D harmonic minor", "D melodic minor",
    "D#", "D# major", "D# minor", "D# natural minor", "D# harmonic minor", "D# melodic minor",
    "E", "E major", "E minor", "E natural minor", "E harmonic minor", "E melodic minor",
    "F", "F major", "F minor", "F natural minor", "F harmonic minor", "F melodic minor",
    "F#", "F# major", "F# minor", "F# natural minor", "F# harmonic minor", "F# melodic minor",
    "G", "G major", "G minor", "G natural minor", "G harmonic minor", "G melodic minor",
    "G#", "G# major", "G# minor", "G# natural minor", "G# harmonic minor", "G# melodic minor",
    "A", "A major", "A minor", "A natural minor", "A harmonic minor", "A melodic minor",
    "A#", "A# major", "A# minor", "A# natural minor", "A# harmonic minor", "A# melodic minor",
    "B", "B major", "B minor", "B natural minor", "B harmonic minor", "B melodic minor"
]

# Dropdown
key = st.selectbox("Key", keys, index=0)

# Compose button
if st.button("Compose Song"):
    with st.spinner("Composing..."):
        wav_bytes = compose_song_wav(key=key, bpm=bpm, bars=bars)
    st.audio(wav_bytes)
    st.download_button("Download song.wav", data=wav_bytes, file_name="song.wav")