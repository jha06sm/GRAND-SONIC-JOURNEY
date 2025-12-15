from googleapiclient.discovery import build

# 🔑 Replace with your own API key from Google Cloud Console
API_KEY = "AIzaSyDv3WrvzLZDcmuKxAbIhzxBeeYn6fOr6VY"

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Emotion → Search query mapping
emotion_to_query = {
    "happy": "happy pop music",
    "sad": "sad acoustic songs",
    "calm": "calm piano music",
    "energetic": "high energy workout music",
    "romantic": "romantic love songs",
    "angry": "heavy metal music",
    "nostalgic": "90s throwback songs",
    "motivated": "workout motivation songs",
    "focus": "study concentration music",
    "party": "party dance hits",
}


def gsj_recommend(emotion: str, max_results: int = 5):
    """
    Fetch YouTube recommendations based on mood/emotion.
    Returns list of {title, url}.
    """
    query = emotion_to_query.get(emotion.lower(), f"{emotion} music")

    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=max_results,
        type="video"
    )
    response = request.execute()

    recommendations = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        recommendations.append({"title": title, "url": url})

    return recommendations
