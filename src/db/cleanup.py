import os
import sqlite3

DB_PATH = "athena.db"


def wipe_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = OFF;")
        cursor.execute("DELETE FROM user_tracks;")
        cursor.execute("DELETE FROM tracks;")
        conn.commit()


def delete_db_file():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"🧨 Deleted {DB_PATH}")
    else:
        print("No DB file found.")
