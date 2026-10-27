"""SQLite persistence for analysis history. Swap the connection for PostgreSQL (psycopg) when multi-user."""
import json
import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone

DB_PATH = os.getenv("DB_PATH", "career_engine.db")


def _conn():
    return sqlite3.connect(DB_PATH)


def init():
    with closing(_conn()) as c, c:
        c.execute("""CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, kind TEXT,
            skills TEXT, top_career TEXT, top_score INTEGER)""")


def save(kind: str, skills: list[str], top_career: str, top_score: int):
    with closing(_conn()) as c, c:
        c.execute("INSERT INTO analyses (created_at, kind, skills, top_career, top_score) VALUES (?,?,?,?,?)",
                  (datetime.now(timezone.utc).isoformat(timespec="seconds"), kind, json.dumps(skills), top_career, top_score))


def recent(limit: int = 10) -> list[dict]:
    with closing(_conn()) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [{**dict(r), "skills": json.loads(r["skills"])} for r in rows]
