import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from typing import Optional
import re
import torchaudio

# Load the MusicGen model
MODEL_NAME = "facebook/musicgen-small"
print("Loading MusicGen model...")
processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = MusicgenForConditionalGeneration.from_pretrained(MODEL_NAME)

# Helper functions
def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def analyze_lyrics(lyrics: str) -> dict:
    lyrics_lower = lyrics.lower()
    mood = "uplifting" if any(word in lyrics_lower for word in ["love", "happy", "smile", "dream"]) else "melancholic"
    keywords = [word for word in lyrics_lower.split() if len(word) > 4][:5]
    return {"mood": mood, "keywords": keywords}

def map_genre_to_style(genre: str, mood: str) -> str:
    styles = {
        "pop": f"{mood} pop instrumental with piano, acoustic guitar, and soft drums",
        "rock": f"{mood} rock instrumental with electric guitars, bass, and drums",
        "edm": f"{mood} EDM instrumental with synths, bass drops, and energetic beats",
        "lofi": f"{mood} lo-fi instrumental with soft keys, vinyl crackle, and chill beats",
        "bollywood": f"{mood} Bollywood-style instrumental with sitar, strings, and gentle percussion"
    }
    return styles.get(genre.lower(), f"{mood} instrumental music")

# Main function
def generate_instrumental_from_lyrics(
    lyrics: str,
    genre: str,
    duration: Optional[int] = 20,
    output_path: str = "output.wav",
    instruments: Optional[list] = None
):
    lyrics_info = analyze_lyrics(lyrics)
    mood = lyrics_info["mood"]
    style_description = map_genre_to_style(genre, mood)

    keywords_str = " ".join(lyrics_info["keywords"])
    prompt = clean_text(f"{style_description}, inspired by themes of {keywords_str}.")

    # Add user-selected instruments to prompt
    if instruments:
        instruments_str = ", ".join(instruments)
        prompt += f", featuring {instruments_str}"

    print(f"Generating music with prompt: {prompt}")

    inputs = processor(text=[prompt], padding=True, return_tensors="pt")
    audio_values = model.generate(**inputs, max_new_tokens=duration * 50)

    sampling_rate = model.config.audio_encoder.sampling_rate
    torchaudio.save(output_path, audio_values[0].cpu(), sampling_rate)

    print(f"Instrumental saved to {output_path}")
    return output_path