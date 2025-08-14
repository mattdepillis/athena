import sqlite3
from pathlib import Path

DB_PATH = Path("athena.db")
SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"  # db/schemas


def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA foreign_keys=OFF;")  # keep v0 friction low
    return c


def init_db() -> None:
    if not SCHEMA_DIR.exists():
        raise RuntimeError(f"Schema directory not found: {SCHEMA_DIR}")

    sql_files = sorted([p for p in SCHEMA_DIR.iterdir() if p.suffix == ".sql"])
    if not sql_files:
        raise RuntimeError(f"No .sql files found in {SCHEMA_DIR}")

    with _conn() as c:
        for f in sql_files:
            with open(f, "r", encoding="utf-8") as fh:
                c.executescript(fh.read())
