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