# db/music/read.py
from __future__ import annotations

from typing import List, Tuple

from db.lib.common import conn


def top_tracks_last_days(
    user_id: str, days: int = 30, limit: int = 50
) -> List[Tuple[str, int]]:
    sql = """
    SELECT ph.track_id, COUNT(*) as plays
    FROM play_history ph
    WHERE ph.user_id=? AND ph.played_at >= datetime('now', ?)
    GROUP BY ph.track_id
    ORDER BY plays DESC
    LIMIT ?
    """
    with conn() as c:
        return c.execute(sql, (user_id, f"-{days} days", limit)).fetchall()


def playlists_needing_refresh(threshold_days: int = 7, limit: int = 200) -> List[str]:
    sql = """
    SELECT playlist_id
    FROM playlist_ingest_queue
    WHERE playlist_id NOT IN (
        SELECT playlist_id FROM playlists
        WHERE last_refreshed >= datetime('now', ?)
    )
    LIMIT ?
    """
    with conn() as c:
        rows = c.execute(sql, (f"-{threshold_days} days", limit)).fetchall()
        return [r[0] for r in rows]
