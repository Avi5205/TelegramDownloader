from collections.abc import Callable
from datetime import UTC, datetime

from models import Channel, ScanResult
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
            self._update_result(result, message)

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
        message,
    ) -> None:
        result.total_messages += 1
        result.scanned_messages += 1

        file_info = self._classify(message)

        if file_info is None:
            return

        category, size = file_info

        result.total_files += 1
        result.total_size += size

        setattr(
            result,
            category,
            getattr(result, category) + 1,
        )

    def _classify(self, message) -> tuple[str, int] | None:
        file = getattr(message, "file", None)

        if file is None:
            return None

        filename = (
            getattr(file, "name", None)
            or getattr(file, "ext", None)
            or getattr(file, "mime_type", None)
        )
        size = getattr(file, "size", 0) or 0

        return classify(filename), size
