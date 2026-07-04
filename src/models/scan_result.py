from dataclasses import dataclass, field
from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class ScanResult:
    """
    Summary produced after scanning a Telegram channel.
    """

    channel_id: int
    channel_name: str

    total_messages: int = 0
    scanned_messages: int = 0

    total_files: int = 0
    total_size: int = 0

    videos: int = 0
    documents: int = 0
    images: int = 0
    audio: int = 0
    archives: int = 0
    others: int = 0

    started_at: datetime = field(default_factory=utc_now)
    completed_at: datetime | None = None

    completed: bool = False

    @property
    def size_mb(self) -> float:
        return self.total_size / (1024 * 1024)

    @property
    def size_gb(self) -> float:
        return self.total_size / (1024 * 1024 * 1024)

    @property
    def duration_seconds(self) -> float:
        if self.completed_at is None:
            return 0.0

        return (self.completed_at - self.started_at).total_seconds()

    @property
    def human_size(self) -> str:
        size = float(self.total_size)

        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size < 1024:
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} PB"
