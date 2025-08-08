# Spotify ETL Design

## Overview
The Spotify ETL module powers Athena's ability to ingest, store, and analyze your listening history, playlist metadata, and profile relationships.  
The design is split into **frequent delta ingestion jobs** and **slower, context-building jobs** to balance freshness, scalability, and API rate limits.

The system:
- **Upserts** global entities (tracks, albums, artists, playlists) to avoid duplicate storage
- Maintains **delta cursors** so we only pull new data
- Tracks **ingest runs** for observability and replay
- Uses **staging_raw** tables for raw JSON capture, enabling re-processing if mapping changes
- Stores **images, audio features, and vendor-specific fields** in JSON initially for speed of iteration
- Stages **playlist IDs** from listening history in a dedicated queue table (`playlist_ingest_queue`) before running the slower playlist job

---

## ETL Job Types

### 1. Play History Job
- **Source:** `/me/player/recently-played`
- **Purpose:** Capture all tracks played since the last ingestion
- **Frequency:** Daily or on manual trigger
- **Tables Written:**
  - `play_history` (fact table, growing over time)
  - `tracks` (upsert)
  - `albums`, `artists`, `track_artists` (upsert)
  - `playlist_ingest_queue` (temporary staging for new playlist IDs)
- **Special Logic:**
  - Stores `context_type` and `context_uri` (e.g., playlist, album, artist, DJ session)
  - Extracts playlist IDs from `context_uri` and adds them to `playlist_ingest_queue` (deduped)
  - Only fetches `audio_features` for tracks missing them
  - Advances a stored **cursor** so we can run true deltas

---

### 2. Playlist Metadata Job
- **Source:** `/me/playlists` + `/playlists/{id}`
- **Purpose:** Store playlist metadata and track composition
- **Frequency:** Weekly or on-demand when new playlists detected from `playlist_ingest_queue`
- **Tables Written:**
  - `playlists`
  - `playlist_tracks` (join table)
- **Special Logic:**
  - Images stored as JSON array (`images_json`)
  - Owner data upserted into `users`
  - Skips refresh if `last_refreshed` < 7 days old
  - Clears processed IDs from `playlist_ingest_queue`

---

### 3. Profile & Friend Graph Job
- **Source:** `/me` + `/users/{id}`
- **Purpose:** Map relationships between you, followed users, and playlist owners
- **Frequency:** Monthly or manual refresh
- **Tables Written:**
  - `users`
  - `user_relationships`
- **Special Logic:**
  - Stores whether a user is “me”
  - Friend relationships as a join table for later graph analytics

---

## Table Schema (v0, additive-friendly)

### `tracks`
| column               | type    | notes |
|----------------------|---------|-------|
| track_id             | TEXT PK | Spotify track ID |
| name                 | TEXT    | Track name |
| album_id             | TEXT    | Album reference |
| duration_ms          | INTEGER | Length |
| popularity           | INTEGER | Spotify popularity score |
| uri                  | TEXT    | Spotify URI |
| is_local             | BOOLEAN | Local file flag |
| audio_features_json  | TEXT    | Raw JSON from `/audio-features` |
| created_at           | TEXT    | Insert timestamp |
| last_updated         | TEXT    | Last upsert timestamp |

---

### `albums`
| album_id     | TEXT PK | Spotify album ID |
| name         | TEXT    | Album name |
| release_date | TEXT    | Release date |
| uri          | TEXT    | Spotify URI |
| images_json  | TEXT    | Array of `{url,width,height}` |
| last_updated | TEXT    | Last upsert timestamp |

---

### `artists`
| artist_id    | TEXT PK | Spotify artist ID |
| name         | TEXT    | Artist name |
| uri          | TEXT    | Spotify URI |
| images_json  | TEXT    | Array of `{url,width,height}` |
| last_updated | TEXT    | Last upsert timestamp |

---

### `track_artists`
| track_id     | TEXT    | Track reference |
| artist_id    | TEXT    | Artist reference |
| PRIMARY KEY  | (track_id, artist_id) |

---

### `play_history`
| play_id      | INTEGER PK | Auto-increment |
| user_id      | TEXT    | User reference |
| track_id     | TEXT    | Track reference |
| played_at    | TEXT    | ISO8601 timestamp |
| context_type | TEXT    | Playlist, album, artist, etc. |
| context_uri  | TEXT    | URI of source context |
| source       | TEXT    | e.g. `spotify` |
| ingested_at  | TEXT    | Timestamp of ingestion |

**Unique Index:** `(user_id, track_id, played_at)` to prevent duplicates.

---

### `playlist_ingest_queue`
| playlist_id  | TEXT PK | Spotify playlist ID |
| detected_at  | TEXT    | When the playlist was detected for ingestion |

---

### `playlists`
| playlist_id  | TEXT PK | Spotify playlist ID |
| name         | TEXT    | Playlist name |
| owner_id     | TEXT    | Creator's user ID |
| owner_type   | TEXT    | 'user', 'spotify', 'brand' |
| public       | BOOLEAN | Public/private flag |
| collaborative| BOOLEAN | Collaboration flag |
| description  | TEXT    | Playlist description |
| uri          | TEXT    | Spotify URI |
| images_json  | TEXT    | Array of `{url,width,height}` |
| last_refreshed | TEXT  | Last metadata pull |

---

## Flow Summary

[play_history_job] ──> Tracks/Albums/Artists
                      └──> Play History table
                      └──> Detect playlist refs → send to playlist_ingest_queue

[playlist_ingest_job] ──> Playlists table
                         └──> Playlist Tracks join table

---

## Next Steps
1. Implement `play_history_job.py` for delta ingestion
2. Implement `playlist_job.py` to pull queued playlists
3. Implement `profile_job.py` for friend graph mapping
