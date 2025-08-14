import os
import sqlite3
from pathlib import Path

DB_PATH = Path("athena.db")


def _conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


# Wipe data but keep schema
def wipe_tables() -> None:
    tables = [
        "play_history",
        "track_artists",
        "tracks",
        "albums",
        "artists",
        # "playlist_tracks",
        "playlists",
        "playlist_ingest_queue",
        # internal tables (optional to wipe):
        "staging_raw",
        "cursors",
        "ingest_runs",
    ]
    with _conn() as c:
        c.execute("PRAGMA foreign_keys = OFF;")
        for t in tables:
            c.execute(f"DELETE FROM {t};")
        c.commit()


# Delete the DB file entirely
def nuke_db() -> None:
    if DB_PATH.exists():
        os.remove(DB_PATH)
