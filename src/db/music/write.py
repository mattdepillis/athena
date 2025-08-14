# db/music/write.py
from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Tuple

from db.lib.common import executemany, now


# ---------- albums ----------
def upsert_albums(albums: Iterable[Dict[str, Any]]) -> int:
    rows = []
    for a in albums:
        rows.append(
            (
                a.get("album_id"),
                a.get("name"),
                a.get("release_date"),
                a.get("uri"),
                json.dumps(a.get("images") or a.get("images_json") or []),
                a.get("last_updated") or now(),
            )
        )
    sql = """
    INSERT INTO albums(album_id, name, release_date, uri, images_json, last_updated)
    VALUES(?, ?, ?, ?, ?, ?)
    ON CONFLICT(album_id) DO UPDATE SET
        name=excluded.name,
        release_date=excluded.release_date,
        uri=excluded.uri,
        images_json=excluded.images_json,
        last_updated=excluded.last_updated
    """
    return executemany(sql, rows)


# ---------- artists ----------
def upsert_artists(artists: Iterable[Dict[str, Any]]) -> int:
    rows = []
    for ar in artists:
        rows.append(
            (
                ar.get("artist_id"),
                ar.get("name"),
                ar.get("uri"),
                json.dumps(ar.get("images") or ar.get("images_json") or []),
                ar.get("last_updated") or now(),
            )
        )
    sql = """
    INSERT INTO artists(artist_id, name, uri, images_json, last_updated)
    VALUES(?, ?, ?, ?, ?)
    ON CONFLICT(artist_id) DO UPDATE SET
        name=excluded.name,
        uri=excluded.uri,
        images_json=excluded.images_json,
        last_updated=excluded.last_updated
    """
    return executemany(sql, rows)


# ---------- tracks ----------
def upsert_tracks(tracks: Iterable[Dict[str, Any]]) -> int:
    rows = []
    for t in tracks:
        rows.append(
            (
                t.get("track_id"),
                t.get("name"),
                t.get("album_id"),
                t.get("duration_ms"),
                t.get("popularity"),
                t.get("uri"),
                t.get("is_local"),
                json.dumps(
                    t.get("audio_features") or t.get("audio_features_json") or None
                ),
                t.get("created_at") or now(),
                t.get("last_updated") or now(),
            )
        )
    sql = """
    INSERT INTO tracks(track_id, name, album_id, duration_ms, popularity, uri, is_local,
                       audio_features_json, created_at, last_updated)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(track_id) DO UPDATE SET
        name=excluded.name,
        album_id=excluded.album_id,
        duration_ms=excluded.duration_ms,
        popularity=excluded.popularity,
        uri=excluded.uri,
        is_local=excluded.is_local,
        audio_features_json=COALESCE(excluded.audio_features_json, tracks.audio_features_json),
        last_updated=excluded.last_updated
    """
    return executemany(sql, rows)


# ---------- many-to-many ----------
def upsert_track_artists(pairs: Iterable[Tuple[str, str]]) -> int:
    rows = [(t, a) for (t, a) in pairs]
    sql = "INSERT OR IGNORE INTO track_artists(track_id, artist_id) VALUES(?, ?)"
    return executemany(sql, rows)


# ---------- facts ----------
def insert_play_history(user_id: str, plays: Iterable[Dict[str, Any]]) -> int:
    rows = []
    for p in plays:
        rows.append(
            (
                user_id,
                p.get("track_id"),
                p.get("played_at"),
                p.get("context_type"),
                p.get("context_uri"),
                p.get("source") or "spotify",  # default
                now(),
            )
        )
    sql = """
    INSERT OR IGNORE INTO play_history
      (user_id, track_id, played_at, context_type, context_uri, source, ingested_at)
    VALUES(?, ?, ?, ?, ?, ?, ?)
    """
    return executemany(sql, rows)


# ---------- queue ----------
def enqueue_playlists(ids: Iterable[str]) -> int:
    rows = [(pid, now()) for pid in set(ids)]
    sql = "INSERT OR IGNORE INTO playlist_ingest_queue(playlist_id, detected_at) VALUES(?, ?)"
    return executemany(sql, rows)
