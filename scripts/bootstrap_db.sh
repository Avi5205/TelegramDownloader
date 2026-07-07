#!/usr/bin/env bash

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT_DIR/src"

echo "Project root: $ROOT_DIR"
echo "SRC dir: $SRC_DIR"

# 1. Ensure directories exist
mkdir -p "$SRC_DIR/database"
mkdir -p "$SRC_DIR/repositories"

# 2. Update config/paths.py with DATA_DIR and DB_PATH if missing
CONFIG_PATHS="$SRC_DIR/config/paths.py"

if [ ! -f "$CONFIG_PATHS" ]; then
  echo "ERROR: $CONFIG_PATHS not found. Please ensure config/paths.py exists."
else
  if ! grep -q "DATA_DIR" "$CONFIG_PATHS"; then
    echo "Updating config/paths.py with DATA_DIR and DB_PATH..."
    cat << 'EOF' >> "$CONFIG_PATHS"

# --- Database paths ---
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "telegram_downloader.db"
EOF
  else
    echo "DATA_DIR already defined in config/paths.py, skipping."
  fi
fi

# 3. Create database/database.py if empty or missing
DB_MODULE="$SRC_DIR/database/database.py"
if [ ! -f "$DB_MODULE" ] || [ ! -s "$DB_MODULE" ]; then
  echo "Creating $DB_MODULE..."
  cat << 'EOF' > "$DB_MODULE"
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
EOF
else
  echo "$DB_MODULE already exists and is non-empty, skipping creation."
fi

# 4. Create repositories

# 4.1 FileRepository
FILE_REPO="$SRC_DIR/repositories/file_repository.py"
if [ ! -f "$FILE_REPO" ]; then
  echo "Creating $FILE_REPO..."
  cat << 'EOF' > "$FILE_REPO"
from datetime import datetime
from typing import Iterable

from database.database import get_connection
from models import FileInfo


class FileRepository:
    def save_files(self, files: Iterable[FileInfo]) -> None:
        conn = get_connection()
        cur = conn.cursor()

        rows = [
            (
                f.message_id,
                f.channel_id,
                f.file_name,
                f.extension,
                f.mime_type,
                f.category,
                f.size,
                f.date.isoformat(),
            )
            for f in files
        ]

        cur.executemany(
            """
            INSERT OR IGNORE INTO files (
                message_id, channel_id, file_name, extension,
                mime_type, category, size, date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        conn.commit()
        conn.close()

    def get_files_for_channel(self, channel_id: int) -> list[FileInfo]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM files WHERE channel_id = ? ORDER BY date ASC",
            (channel_id,),
        )
        rows = cur.fetchall()
        conn.close()

        return [
            FileInfo(
                message_id=row["message_id"],
                file_name=row["file_name"],
                category=row["category"],
                extension=row["extension"],
                size=row["size"],
                date=datetime.fromisoformat(row["date"]),
                mime_type=row["mime_type"],
                channel_id=row["channel_id"],
            )
            for row in rows
        ]
EOF
else
  echo "$FILE_REPO already exists, skipping."
fi

# 4.2 ScanRepository
SCAN_REPO="$SRC_DIR/repositories/scan_repository.py"
if [ ! -f "$SCAN_REPO" ]; then
  echo "Creating $SCAN_REPO..."
  cat << 'EOF' > "$SCAN_REPO"
from datetime import datetime

from database.database import get_connection


class ScanRepository:
    def save_scan_summary(self, channel_id: int, scanned_at: datetime, total_files: int, total_size: int) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO scan_results (channel_id, scanned_at, total_files, total_size)
            VALUES (?, ?, ?, ?)
            """,
            (channel_id, scanned_at.isoformat(), total_files, total_size),
        )
        conn.commit()
        conn.close()

    def get_last_scan_time(self, channel_id: int) -> datetime | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT scanned_at
            FROM scan_results
            WHERE channel_id = ?
            ORDER BY scanned_at DESC
            LIMIT 1
            """,
            (channel_id,),
        )
        row = cur.fetchone()
        conn.close()

        if row is None:
            return None

        return datetime.fromisoformat(row["scanned_at"])
EOF
else
  echo "$SCAN_REPO already exists, skipping."
fi

# 4.3 ChannelRepository
CHANNEL_REPO="$SRC_DIR/repositories/channel_repository.py"
if [ ! -f "$CHANNEL_REPO" ]; then
  echo "Creating $CHANNEL_REPO..."
  cat << 'EOF' > "$CHANNEL_REPO"
from database.database import get_connection
from models import Channel


class ChannelRepository:
    def save_channels(self, channels: list[Channel]) -> None:
        conn = get_connection()
        cur = conn.cursor()
        rows = [
            (c.id, c.title, c.username)
            for c in channels
        ]
        cur.executemany(
            """
            INSERT OR REPLACE INTO channels (id, title, username)
            VALUES (?, ?, ?)
            """,
            rows,
        )
        conn.commit()
        conn.close()

    def get_channels(self) -> list[Channel]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, username FROM channels")
        rows = cur.fetchall()
        conn.close()

        return [
            Channel(
                id=row["id"],
                title=row["title"],
                username=row["username"],
            )
            for row in rows
        ]
EOF
else
  echo "$CHANNEL_REPO already exists, skipping."
fi

# 4.4 DownloadRepository
DOWNLOAD_REPO="$SRC_DIR/repositories/download_repository.py"
if [ ! -f "$DOWNLOAD_REPO" ]; then
  echo "Creating $DOWNLOAD_REPO..."
  cat << 'EOF' > "$DOWNLOAD_REPO"
from datetime import datetime

from database.database import get_connection


class DownloadRepository:
    def record_download(self, file_id: int | None, destination: str, status: str, bytes_written: int) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO download_records (file_id, destination, downloaded_at, status, bytes_written)
            VALUES (?, ?, ?, ?, ?)
            """,
            (file_id, destination, datetime.now().isoformat(), status, bytes_written),
        )
        conn.commit()
        conn.close()
EOF
else
  echo "$DOWNLOAD_REPO already exists, skipping."
fi

# 4.5 SettingsRepository
SETTINGS_REPO="$SRC_DIR/repositories/settings_repository.py"
if [ ! -f "$SETTINGS_REPO" ]; then
  echo "Creating $SETTINGS_REPO..."
  cat << 'EOF' > "$SETTINGS_REPO"
from database.database import get_connection


class SettingsRepository:
    def get(self, key: str) -> str | None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cur.fetchone()
        conn.close()
        return row["value"] if row else None

    def set(self, key: str, value: str) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value),
        )
        conn.commit()
        conn.close()
EOF
else
  echo "$SETTINGS_REPO already exists, skipping."
fi

echo "Bootstrap complete. Remember to:"
echo " - Call init_schema() from main.py at startup."
echo " - Wire repositories into your scanner and download flow."