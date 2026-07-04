from dataclasses import dataclass


@dataclass(slots=True)
class ScanResult:
    """
    Summary produced after scanning a Telegram channel.
    """

    total_messages: int = 0
    total_files: int = 0

    total_size: int = 0

    videos: int = 0
    documents: int = 0
    images: int = 0
    audio: int = 0
    archives: int = 0

    scanned_messages: int = 0

    completed: bool = False