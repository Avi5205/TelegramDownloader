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