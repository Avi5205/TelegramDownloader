from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ScannedFile:
    """A single downloadable file discovered during channel scanning."""

    message_id: int
    channel_id: int
    filename: str
    extension: str
    size: int
    category: str
    date: datetime | None = None
    mime_type: str = ""
    download_path: str | None = None
