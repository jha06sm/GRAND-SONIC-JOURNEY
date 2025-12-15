import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re

CLIENT_ID = "b7a7cb89831d4729992eb7ce1b313bfd"
CLIENT_SECRET = "a32b9deef5c743629aae5776b57c09a3"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

def get_playlist_id(url: str) -> str:
    """
    Extracts the playlist ID from a Spotify URL or URI.
    """
    match = re.search(r"(playlist/|:playlist:)([a-zA-Z0-9]+)", url)
    if match:
        return match.group(2)
    return url  # if already just the ID

def fetch_spotify_tracks(url: str, limit=100):
    playlist_id = get_playlist_id(url)
    results = sp.playlist_items(playlist_id, limit=limit)

    tracks = []
    while results:
        for item in results["items"]:
            track = item["track"]
            if track:  # skip None
                tracks.append({
                    "id": track["id"],
                    "name": track["name"],
                    "artist": ", ".join([a["name"] for a in track["artists"]]),
                    "album": track["album"]["name"],
                    "release_date": track["album"]["release_date"],
                    "popularity": track["popularity"],
                    "url": track["external_urls"]["spotify"]
                })
        if results["next"]:
            results = sp.next(results)
        else:
            results = None

    return pd.DataFrame(tracks)


if __name__ == "__main__":
    url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
    df = fetch_spotify_tracks(url)
    print(df.head())
