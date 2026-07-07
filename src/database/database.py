from pathlib import Path
import sqlite3

from config.paths import DB_PATH


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            username TEXT,
            last_scanned_at TEXT
        );

        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            file_name TEXT,
            extension TEXT,
            mime_type TEXT,
            category TEXT,
            size INTEGER,
            date TEXT,
            UNIQUE(channel_id, message_id)
        );

        CREATE TABLE IF NOT EXISTS scan_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER NOT NULL,
            scanned_at TEXT NOT NULL,
            total_files INTEGER,
            total_size INTEGER
        );

        CREATE TABLE IF NOT EXISTS download_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER,
            destination TEXT,
            downloaded_at TEXT,
            status TEXT,
            bytes_written INTEGER
        );

        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );

        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER NOT NULL
        );
        """
    )

    # Initialize schema_version if empty
    cur.execute("SELECT COUNT(*) AS c FROM schema_version")
    row = cur.fetchone()
    if row["c"] == 0:
        cur.execute("INSERT INTO schema_version (version) VALUES (1)")

    conn.commit()
    conn.close()