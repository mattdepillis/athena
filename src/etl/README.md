# Spotify ETL Design

## Overview
The Spotify ETL module powers Athena's ability to ingest, store, and analyze your listening history, playlist metadata, and profile relationships.  
The design is split into **frequent delta ingestion** jobs and **slower, context-building** jobs to balance freshness, scalability, and API rate limits.

---

## ETL Job Types

### 1. Play History Job
- **Source:** `/me/player/recently-played`
- **Purpose:** Capture tracks played since the last ingestion
- **Frequency:** Daily or on manual trigger
- **Tables Written:**
  - `play_history` (fact table)
  - `tracks` (upsert)
  - `albums`, `artists`, `track_artists` (upsert)
- **Special Logic:**
  - Stores `context_type` and `context_uri` (e.g., playlist, album)
  - Detects new playlist IDs for later ingestion

---

### 2. Playlist Metadata Job
- **Source:** `/me/playlists` + `/playlists/{id}`
- **Purpose:** Store playlist metadata and track composition
- **Frequency:** Weekly or on-demand when new playlists detected
- **Tables Written:**
  - `playlists`
  - `playlist_tracks` (join table)

---

### 3. Profile & Friend Graph Job
- **Source:** `/me` + `/users/{id}`
- **Purpose:** Map relationships between you, followed users, and playlist owners
- **Frequency:** Monthly or manual refresh
- **Tables Written:**
  - `users`
  - `user_relationships`

---

## Table Schema

### `tracks`
| column     | type    | notes |
|------------|---------|-------|
| track_id   | TEXT PK | Spotify track ID |
| name       | TEXT    | Track name |
| album_id   | TEXT FK | Album reference |
| uri        | TEXT    | Spotify URI |

### `albums`
| album_id   | TEXT PK | Spotify album ID |
| name       | TEXT    | Album name |
| release_date | TEXT  | Release date |
| image_url	 | TEXT    | Largest available image |

### `artists`
| artist_id  | TEXT PK | Spotify artist ID |
| name       | TEXT    | Artist name |
| image_url	 | TEXT    | Largest available image |

### `track_artists`
| track_id   | TEXT FK | Track reference |
| artist_id  | TEXT FK | Artist reference |

### `play_history`
| played_at  | TEXT    | Timestamp |
| track_id   | TEXT FK | Track reference |
| context_type | TEXT  | Playlist, album, artist, etc. |
| context_uri | TEXT   | URI of source context |

### `playlists`
| playlist_id | TEXT PK | Spotify playlist ID |
| name        | TEXT    | Playlist name |
| owner_id    | TEXT    | Creator's user ID |
| owner_type  | TEXT    | 'user', 'spotify', 'brand' |
| public      | BOOLEAN | Public/private flag |
| collaborative | BOOLEAN | Collaboration flag |

### `playlist_tracks`
| playlist_id | TEXT FK | Playlist reference |
| track_id    | TEXT FK | Track reference |
| added_at    | TEXT    | When track was added |

### `users`
| user_id     | TEXT PK | Spotify user ID |
| display_name| TEXT    | User display name |

### `user_relationships`
| user_id     | TEXT FK | User reference |
| friend_id   | TEXT FK | Followed user ID |

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
