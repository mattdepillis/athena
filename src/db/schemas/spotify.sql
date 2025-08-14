-- Schema definitions for tables related to spotify / other music service data

CREATE TABLE IF NOT EXISTS tracks (
  track_id TEXT PRIMARY KEY,
  name TEXT,
  album_id TEXT,
  duration_ms INTEGER,
  popularity INTEGER,
  uri TEXT,
  is_local BOOLEAN,
  audio_features_json TEXT,
  created_at TEXT,
  last_updated TEXT
);

CREATE TABLE IF NOT EXISTS albums (
  album_id TEXT PRIMARY KEY,
  name TEXT,
  release_date TEXT,
  uri TEXT,
  images_json TEXT,
  last_updated TEXT
);

CREATE TABLE IF NOT EXISTS artists (
  artist_id TEXT PRIMARY KEY,
  name TEXT,
  uri TEXT,
  images_json TEXT,
  last_updated TEXT
);

CREATE TABLE IF NOT EXISTS track_artists (
  track_id TEXT,
  artist_id TEXT,
  PRIMARY KEY(track_id, artist_id)
);

CREATE TABLE IF NOT EXISTS play_history (
  play_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT,
  track_id TEXT,
  played_at TEXT,
  context_type TEXT,
  context_uri TEXT,
  source TEXT DEFAULT 'spotify',
  ingested_at TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_play ON play_history(user_id, track_id, played_at);
CREATE INDEX IF NOT EXISTS idx_play_user_time ON play_history(user_id, played_at DESC);

CREATE TABLE IF NOT EXISTS playlist_ingest_queue (
  playlist_id TEXT PRIMARY KEY,
  detected_at TEXT
);

CREATE TABLE IF NOT EXISTS playlists (
  playlist_id TEXT PRIMARY KEY,
  name TEXT,
  owner_id TEXT,
  owner_type TEXT,
  public BOOLEAN,
  collaborative BOOLEAN,
  description TEXT,
  uri TEXT,
  images_json TEXT,
  last_refreshed TEXT
);

-- TEMP SCHEMA FOR NOW (AS OF 8/13)
CREATE TABLE IF NOT EXISTS playlist_tracks (
  playlist_id TEXT NOT NULL,
  track_id TEXT NOT NULL,
  added_at TEXT,            -- when it was added to the playlist (Spotify metadata)
  added_by_user_id TEXT,    -- who added it, if available
  PRIMARY KEY (playlist_id, track_id)
);
CREATE INDEX IF NOT EXISTS idx_playlist_tracks_playlist
  ON playlist_tracks(playlist_id);

