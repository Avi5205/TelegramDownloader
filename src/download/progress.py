from dataclasses import dataclass
from datetime import timedelta


@dataclass(slots=True)
class DownloadResult:
    total_files: int
    downloaded_files: int
    failed_files: int
    total_bytes: int
    elapsed: timedelta


@dataclass(slots=True)
class DownloadProgress:
    current_file: str
    completed_files: int
    total_files: int
    downloaded_bytes: int
    total_bytes: int
