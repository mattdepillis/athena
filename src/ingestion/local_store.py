import json
from datetime import datetime
from pathlib import Path

NOTES_PATH = Path.home() / ".athena" / "notes.jsonl"
NOTES_PATH.parent.mkdir(parents=True, exist_ok=True)

def save_note(text: str):
    note = {
        "text": text,
        "timestamp": datetime.now().isoformat()
    }
    with open(NOTES_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(note) + "\n")
