import streamlit as st
from gen.lyrics import generate_lyrics

st.title("📝 Lyrics Generator (English & Hindi)")
lang = st.radio("Language", ["English","Hindi"], horizontal=True)
theme = st.text_input("Theme / Prompt", "city rain and memories")
style = st.selectbox("Style", ["romantic","hip-hop","ghazal","indie-pop","motivational"])
mood = st.selectbox("Mood (Emotion)", ["happy", "sad", "nostalgic", "romantic", "energetic", "melancholic"])
rhyme = st.selectbox("Rhyme Scheme", ["AABB","ABAB","Free"])
verses = st.slider("Verses", 1, 4, 2)
hook = st.checkbox("Include Chorus", True)
tokens = st.slider("Max tokens", 50, 400, 180)

if st.button("Generate Lyrics"):
    with st.spinner("Generating..."):
        lyrics = generate_lyrics(theme, language=lang, style=style, rhyme_scheme=rhyme, verses=verses, hook=hook, max_new_tokens=tokens)
    st.text_area("Lyrics", value=lyrics, height=400)
    st.download_button("Download .txt", data=lyrics, file_name="lyrics.txt")