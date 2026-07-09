from __future__ import annotations

from typing import Iterable

from database.transaction import transaction
from models.file_info import FileInfo


class FileRepository:
    """
    Repository responsible for file persistence.
    """

    INSERT_SQL = """
    INSERT OR IGNORE INTO files
    (
        message_id,
        channel_id,
        file_name,
        extension,
        mime_type,
        category,
        size,
        date
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    SELECT_BY_CHANNEL = """
    SELECT
        message_id,
        channel_id,
        file_name,
        extension,
        mime_type,
        category,
        size,
        date
    FROM files
    WHERE channel_id = ?
    ORDER BY date DESC
    """

    def save_files(
            self,
            files: Iterable[FileInfo],
    ) -> None:
        rows = [
            (
                file.message_id,
                file.channel_id,
                file.file_name,
                file.extension,
                file.mime_type,
                file.category,
                file.size,
                file.date.isoformat(),
            )
            for file in files
        ]

        if not rows:
            return

        with transaction() as conn:
            conn.executemany(
                self.INSERT_SQL,
                rows,
            )

    def get_files_for_channel(
            self,
            channel_id: int,
    ) -> list[FileInfo]:
        with transaction() as conn:
            cursor = conn.execute(
                self.SELECT_BY_CHANNEL,
                (channel_id,),
            )

            rows = cursor.fetchall()

        return [
            FileInfo(
                message_id=row["message_id"],
                channel_id=row["channel_id"],
                file_name=row["file_name"],
                extension=row["extension"],
                mime_type=row["mime_type"],
                category=row["category"],
                size=row["size"],
                date=row["date"],
            )
            for row in rows
        ]
