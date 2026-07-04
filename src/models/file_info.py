from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class FileInfo:
    """
    Represents a downloadable Telegram file.
    """

    message_id: int
    file_name: str
    category: str
    extension: str
    size: int
    date: datetime
    mime_type: str | None
    channel_id: int

    @property
    def size_mb(self) -> float:
        return self.size / (1024 * 1024)

    @property
    def human_size(self) -> str:
        size = float(self.size)

        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size < 1024:
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} PB"
