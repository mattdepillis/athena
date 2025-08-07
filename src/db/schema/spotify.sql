-- Global track metadata
CREATE TABLE IF NOT EXISTS tracks (
    track_id TEXT PRIMARY KEY,
    name TEXT,
    artist TEXT,
    audio_features JSON,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User-specific engagement
CREATE TABLE IF NOT EXISTS user_tracks (
    user_id TEXT,
    track_id TEXT,
    is_liked BOOLEAN,
    play_count INTEGER,
    first_seen TIMESTAMP,
    last_played TIMESTAMP,
    playlists JSON,
    PRIMARY KEY (user_id, track_id),
    FOREIGN KEY (track_id) REFERENCES tracks(track_id)
);