from __future__ import annotations

import asyncio
import logging
import time
from datetime import timedelta
from pathlib import Path
from typing import Callable, Iterable, List

from download.progress import DownloadProgress, DownloadResult
from models import FileInfo
from repositories.download_repository import DownloadRepository  # NEW
from telegram.client import TelegramService

logger = logging.getLogger(__name__)


class DownloadManager:
    """Orchestrates downloads by delegating actual media transfer to TelegramService.

    Responsibilities:
    - Validate input
    - Call TelegramService.download_media(file_info, destination)
    - Report progress via a callback
    - Return a DownloadResult summary

    Note: TelegramService must be provided by the caller to ensure a single
    Telethon client is used across the application.
    """

    def __init__(self, telegram_service: TelegramService):
        if telegram_service is None:
            raise ValueError("telegram_service is required")
        self._telegram_service = telegram_service
        self._download_repo = DownloadRepository()  # NEW

    async def download(
            self,
            files: Iterable[FileInfo],
            destination: Path,
            progress_callback: Callable[[DownloadProgress], None] | None = None,
    ) -> DownloadResult:
        files_list: List[FileInfo] = list(files)
        total_files = len(files_list)

        if total_files == 0:
            return DownloadResult(
                total_files=0,
                downloaded_files=0,
                failed_files=0,
                total_bytes=0,
                elapsed=timedelta(0),
            )

        dest = Path(destination)
        dest.mkdir(parents=True, exist_ok=True)

        if not dest.is_dir():
            raise ValueError(f"Destination {dest} is not a directory")

        downloaded_files = 0
        failed_files = 0
        downloaded_bytes = 0
        total_bytes = sum((f.size or 0) for f in files_list)

        start = time.monotonic()

        for file_info in files_list:
            current_file_name = file_info.file_name or f"file_{file_info.message_id}"

            # emit progress before starting file
            if progress_callback:
                progress_callback(
                    DownloadProgress(
                        current_file=current_file_name,
                        completed_files=downloaded_files,
                        failed_files=failed_files,
                        total_files=total_files,
                        downloaded_bytes=downloaded_bytes,
                        total_bytes=total_bytes,
                    )
                )

            try:
                dest_path = dest / current_file_name
                bytes_written = await self._telegram_service.download_media(file_info, dest_path)

                downloaded_files += 1
                downloaded_bytes += int(bytes_written)

                # record successful download (file_id None for now)
                self._download_repo.record_download(
                    file_id=None,
                    destination=str(dest_path),
                    status="success",
                    bytes_written=int(bytes_written),
                )

            except Exception as exc:  # Log and continue with next file
                failed_files += 1
                logger.exception("Failed to download %s: %s", current_file_name, exc)

                # record failed download
                self._download_repo.record_download(
                    file_id=None,
                    destination=str(dest / current_file_name),
                    status="failed",
                    bytes_written=0,
                )

            # emit progress after finishing file
            if progress_callback:
                progress_callback(
                    DownloadProgress(
                        current_file=current_file_name,
                        completed_files=downloaded_files,
                        failed_files=failed_files,
                        total_files=total_files,
                        downloaded_bytes=downloaded_bytes,
                        total_bytes=total_bytes,
                    )
                )

            # Yield to event loop briefly to keep UI responsive
            await asyncio.sleep(0)

        elapsed = timedelta(seconds=(time.monotonic() - start))

        return DownloadResult(
            total_files=total_files,
            downloaded_files=downloaded_files,
            failed_files=failed_files,
            total_bytes=downloaded_bytes,
            elapsed=elapsed,
        )
