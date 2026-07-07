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