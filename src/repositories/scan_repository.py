from __future__ import annotations

from datetime import datetime

from database.transaction import transaction


class ScanRepository:
    INSERT_SQL = """
    INSERT INTO scan_results
    (
        channel_id,
        scanned_at,
        total_files,
        total_size
    )
    VALUES (?, ?, ?, ?)
    """

    def save_scan_summary(
            self,
            channel_id: int,
            scanned_at: datetime,
            total_files: int,
            total_size: int,
    ) -> None:
        with transaction() as conn:
            conn.execute(
                self.INSERT_SQL,
                (
                    channel_id,
                    scanned_at.isoformat(),
                    total_files,
                    total_size,
                ),
            )
