import os
import sqlite3
from pathlib import Path

DB_PATH = "athena.db"
BASE_DIR = Path(__file__).resolve().parent  # src/db/
SCHEMA_PATH = BASE_DIR / "schema"  # src/db/schema


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        for filename in sorted(os.listdir(SCHEMA_PATH)):
            if filename.endswith(".sql"):
                with open(os.path.join(SCHEMA_PATH, filename), "r") as f:
                    sql = f.read()
                    conn.executescript(sql)
