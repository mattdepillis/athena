# db/common.py
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Sequence

DB_PATH = Path("athena.db")


def conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA foreign_keys=OFF;")  # fewer headaches in v0
    return c


# ---------- timestamps ----------
def now() -> str:
    return datetime.now().isoformat(timespec="seconds") + "Z"


# ---------- ingest runs ----------
def start_run(job: str, user_id: str) -> int:
    with conn() as c:
        c.execute(
            """
            INSERT INTO ingest_runs(job, user_id, started_at, status)
            VALUES(?, ?, ?, 'running')
        """,
            (job, user_id, now()),
        )
        return c.execute("SELECT last_insert_rowid()").fetchone()[0]


def finish_run(
    run_id: int,
    rows_written: int = 0,
    status: str = "success",
    error: Optional[str] = None,
) -> None:
    with conn() as c:
        c.execute(
            """
            UPDATE ingest_runs
            SET finished_at=?, rows_written=?, status=?, error=?
            WHERE run_id=?
        """,
            (now(), rows_written, status, error, run_id),
        )


# ---------- cursors (delta checkpoints) ----------
def get_cursor(job: str, user_id: str) -> Optional[str]:
    with conn() as c:
        row = c.execute(
            "SELECT cursor_value FROM cursors WHERE job=? AND user_id=?", (job, user_id)
        ).fetchone()
        return row[0] if row else None


def set_cursor(job: str, user_id: str, cursor_value: str) -> None:
    with conn() as c:
        c.execute(
            """
            INSERT INTO cursors(job, user_id, cursor_value)
            VALUES(?, ?, ?)
            ON CONFLICT(job, user_id) DO UPDATE SET cursor_value=excluded.cursor_value
        """,
            (job, user_id, cursor_value),
        )


# ---------- staging (raw payload capture) ----------
def stage_raw(job: str, payload_json: str) -> None:
    with conn() as c:
        c.execute(
            """
            INSERT INTO staging_raw(job, payload_json, received_at)
            VALUES(?, ?, ?)
        """,
            (job, payload_json, now()),
        )


# ---------- generic helpers (nice to have) ----------
def executemany(sql: str, rows: Sequence[Sequence[Any]]) -> int:
    if not rows:
        return 0
    with conn() as c:
        c.executemany(sql, rows)
        return c.total_changes


def execute(sql: str, params: Sequence[Any] | None = None) -> int:
    with conn() as c:
        c.execute(sql, params or [])
        return c.total_changes
