from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from models import Channel, FileInfo, ScanResult
from telegram.client import TelegramService
from utils.file_classifier import classify


ProgressCallback = Callable[[ScanResult], None]


class TelegramScanner:
    """
    Scans Telegram channel messages and produces aggregate file statistics.
    """

    def __init__(self, service: TelegramService):
        self._service = service

    async def scan_channel(
        self,
        channel: Channel,
        progress_callback: ProgressCallback | None = None,
    ) -> ScanResult:
        result = ScanResult(
            channel_id=channel.id,
            channel_name=channel.title,
        )

        entity = await self._service.get_entity(
            channel.username or channel.id
        )

        async for message in self._service.iter_messages(entity):
            file_info = self._build_file_info(channel, message)

            self._update_result(result, file_info)

            if (
                progress_callback is not None
                and result.scanned_messages % 250 == 0
            ):
                progress_callback(result)

        result.completed = True
        result.completed_at = datetime.now(UTC)

        if progress_callback is not None:
            progress_callback(result)

        return result

    def _update_result(
        self,
        result: ScanResult,
        file_info: FileInfo | None,
    ) -> None:
        result.total_messages += 1
        result.scanned_messages += 1

        if file_info is None:
            return

        result.files.append(file_info)
        result.total_files += 1
        result.total_size += file_info.size

        setattr(
            result,
            file_info.category,
            getattr(result, file_info.category) + 1,
        )

    def _build_file_info(
        self,
        channel: Channel,
        message,
    ) -> FileInfo | None:
        file = getattr(message, "file", None)

        if file is None:
            return None

        message_id = getattr(message, "id")
        extension = self._extension(file)
        file_name = self._file_name(file, message_id, extension)
        size = getattr(file, "size", 0) or 0
        mime_type = getattr(file, "mime_type", None)
        date = getattr(message, "date", None) or datetime.now(UTC)

        return FileInfo(
            message_id=message_id,
            file_name=file_name,
            category=classify(file_name or extension or mime_type),
            extension=extension,
            size=size,
            date=date,
            mime_type=mime_type,
            channel_id=channel.id,
        )

    def _file_name(
        self,
        file,
        message_id: int,
        extension: str,
    ) -> str:
        file_name = getattr(file, "name", None)

        if file_name:
            return file_name

        return f"telegram-file-{message_id}{extension}"

    def _extension(
        self,
        file,
    ) -> str:
        extension = getattr(file, "ext", None)

        if extension:
            return extension.lower()

        file_name = getattr(file, "name", None)

        if file_name:
            return Path(file_name).suffix.lower()

        return ""
