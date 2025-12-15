from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

def generate_lyrics(
    title: str,
    mood: str = "neutral",
    language: str = "English",
    style: str = None,
    rhyme_scheme: str = None,
    verses: int = 2,
    hook: bool = True,
    max_new_tokens: int = 200
):
    

    # Build the song structure dynamically
    structure = ""
    for i in range(1, verses + 1):
        structure += f"Verse {i}\n"
        if hook:
            structure += f"Chorus {i}\n"
    if verses < 2:
        structure += "Bridge\n"  # always add a bridge if less than 2 verses

    # Build the prompt
    prompt = f"""
Write a {style if style else ''} song in {language} about '{title}'.
Mood: {mood}.
Structure:
{structure.strip()}

"""
    if rhyme_scheme and rhyme_scheme != "Free":
        prompt += f"Use the {rhyme_scheme} rhyme scheme throughout.\n"

    prompt += "Generate creative, engaging lyrics following the structure above."

    # Call OpenAI
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative lyrics generator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_new_tokens,
        temperature=0.9,
        top_p=0.95
    )

    return response.choices[0].message.content


if __name__ == "__main__":
     title = input("🎵 Enter song title: ")
     mood = input("👉 Enter mood (happy, sad, romantic, motivational): ")
     language = input("🌍 Enter language (default = English): ") or "English"
     lyrics = generate_lyrics(title, mood, language) 
     print("\n==================== 🎶 Generated Song 🎶 ====================")
     print(f"🎼 Title: {title}\n")
     print(lyrics)