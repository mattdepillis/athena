import os

from dotenv import load_dotenv

load_dotenv()  # Only once at top level


def get_spotify_credentials():
    return {
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "redirect_uri": os.getenv("SPOTIPY_REDIRECT_URI"),
        "cache_path": os.path.expanduser("~/.athena/spotify_tokens"),
    }
