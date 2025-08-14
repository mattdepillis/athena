-- Schema definitions for tables internal to DB ops + ETL processes

CREATE TABLE IF NOT EXISTS ingest_runs (
  run_id INTEGER PRIMARY KEY AUTOINCREMENT,
  job TEXT, user_id TEXT,
  started_at TEXT, finished_at TEXT,
  rows_written INTEGER, status TEXT, error TEXT
);

CREATE TABLE IF NOT EXISTS cursors (
  job TEXT, user_id TEXT, cursor_value TEXT,
  PRIMARY KEY (job, user_id)
);

CREATE TABLE IF NOT EXISTS staging_raw (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job TEXT, payload_json TEXT, received_at TEXT
);