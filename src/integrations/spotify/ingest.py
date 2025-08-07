import json
import os

from spotipy import Spotify

from core.scopes import SPOTIFY_SCOPES
from integrations.spotify.auth import get_spotify_session

# CACHE_PATH = os.path.expanduser("~/.athena/spotify_tokens")
OUTPUT_PATH = "spotify_liked.json"


def fetch_liked_songs(sp: Spotify, limit=50):
    liked = []
    offset = 0

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = results.get("items", [])
        if not items:
            break

        for item in items:
            track = item["track"]
            liked.append(
                {
                    "id": track["id"],
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "added_at": item["added_at"],
                    "uri": track["uri"],
                }
            )

        offset += limit
        if offset >= results["total"]:
            break

    return liked


def run():
    print("🔐 Authenticating...")
    sp = get_spotify_session([SPOTIFY_SCOPES["default"]])

    print("🎧 Fetching liked songs...")
    liked_songs = fetch_liked_songs(sp)

    print(f"✅ Retrieved {len(liked_songs)} liked songs.")

    with open(OUTPUT_PATH, "w") as f:
        json.dump(liked_songs, f, indent=2)

    print(f"💾 Saved to {OUTPUT_PATH}")
