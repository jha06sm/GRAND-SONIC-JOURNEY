import streamlit as st
import os
import sys

# Ensure the 'gen' folder is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from gen.instrumental import generate_instrumental_from_lyrics

# ---------------- Page Config ----------------
st.set_page_config(page_title="🎹 Generate Instrumental", layout="centered")

st.title("🎹 Lyrics to Instrumental Music")
st.markdown("Enter your lyrics, select a genre, and choose instruments to generate a full instrumental track.")

# ---------------- Load instruments ----------------
instruments_file = os.path.join(root_dir, "data", "instruments_list.txt")
if os.path.isfile(instruments_file):
    with open(instruments_file, "r", encoding="utf-8") as f:
        instruments_options = [line.strip() for line in f if line.strip()]
else:
    st.warning(f"instruments_list.txt not found at: {instruments_file}. Using fallback instruments.")
    instruments_options = ["Guitar", "Tabla", "Piano", "Violin", "Drum", "Dholak"]

# ---------------- User Inputs ----------------
lyrics = st.text_area("✏ Enter Lyrics", placeholder="Type your song lyrics here...")
genre = st.selectbox("🎼 Select Genre", ["Pop", "Rock", "EDM", "LoFi", "Bollywood"])
selected_instruments = st.multiselect("🎻 Select Instruments", instruments_options)
duration = st.slider("⏱ Duration (seconds)", 10, 60, 20)

# Output file path
output_path = os.path.join(root_dir, "generated_instrumental.wav")

# ---------------- Generate Button ----------------
if st.button("🎶 Generate Instrumental"):
    if not lyrics.strip():
        st.warning("Please enter some lyrics first.")
    elif not selected_instruments:
        st.warning("Please select at least one instrument.")
    else:
        with st.spinner("Generating instrumental... please wait ⏳"):
            try:
                file_path = generate_instrumental_from_lyrics(
                    lyrics=lyrics,
                    genre=genre,
                    duration=duration,
                    output_path=output_path,
                    instruments=selected_instruments  # Pass selected instruments
                )
                st.success("Instrumental generated successfully! 🎉")
                st.audio(file_path, format="audio/wav")

                with open(file_path, "rb") as f:
                    st.download_button(
                        label="💾 Download Instrumental",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="audio/wav"
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")