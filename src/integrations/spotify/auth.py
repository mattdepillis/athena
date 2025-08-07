from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from core.config import get_spotify_credentials


def get_spotify_session(scopes: list[str]) -> Spotify:
    scope_str = " ".join(scopes)
    return Spotify(
        auth_manager=SpotifyOAuth(**get_spotify_credentials(), scope=scope_str)
    )
