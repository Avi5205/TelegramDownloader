import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime

from models import Channel
from telegram.scanner import TelegramScanner


@dataclass(slots=True)
class FakeFile:
    name: str | None
    ext: str | None
    size: int
    mime_type: str | None = None


@dataclass(slots=True)
class FakeMessage:
    id: int
    date: datetime
    file: FakeFile | None = None


class FakeService:
    def __init__(
            self,
            messages: list[FakeMessage],
    ):
        self.messages = messages
        self.requested_entity_id = None

    async def get_entity(self, entity_id):
        self.requested_entity_id = entity_id
        return entity_id

    async def iter_messages(self, entity):
        for message in self.messages:
            yield message


def test_scanner_streams_messages_and_counts_files() -> None:
    asyncio.run(_scan_messages_and_count_files())


async def _scan_messages_and_count_files() -> None:
    first_date = datetime(2026, 1, 1, tzinfo=UTC)
    second_date = datetime(2026, 1, 2, tzinfo=UTC)
    third_date = datetime(2026, 1, 3, tzinfo=UTC)
    fourth_date = datetime(2026, 1, 4, tzinfo=UTC)
    messages = [
        FakeMessage(1, first_date),
        FakeMessage(
            2,
            second_date,
            FakeFile("clip.mp4", ".mp4", 100, "video/mp4"),
        ),
        FakeMessage(
            3,
            third_date,
            FakeFile("book.pdf", ".pdf", 200, "application/pdf"),
        ),
        FakeMessage(
            4,
            fourth_date,
            FakeFile(None, ".jpg", 300, "image/jpeg"),
        ),
    ]
    service = FakeService(messages)
    scanner = TelegramScanner(service)
    channel = Channel(
        id=123,
        title="Movies",
        username="movies",
        unread_count=0,
        is_channel=True,
        is_group=False,
    )

    result = await scanner.scan_channel(channel)

    assert service.requested_entity_id == "movies"
    assert result.channel_id == 123
    assert result.channel_name == "Movies"
    assert result.total_messages == 4
    assert result.scanned_messages == 4
    assert result.total_files == 3
    assert result.total_size == 600
    assert result.videos == 1
    assert result.documents == 1
    assert result.images == 1
    assert result.completed is True
    assert result.completed_at is not None
    assert len(result.files) == 3
    assert result.files[0].message_id == 2
    assert result.files[0].file_name == "clip.mp4"
    assert result.files[0].category == "videos"
    assert result.files[0].extension == ".mp4"
    assert result.files[0].size == 100
    assert result.files[0].date == second_date
    assert result.files[0].mime_type == "video/mp4"
    assert result.files[0].channel_id == 123
    assert result.files[2].file_name == "telegram-file-4.jpg"
    assert result.files[2].category == "images"


def test_scanner_reports_progress_every_250_messages_and_at_completion() -> None:
    asyncio.run(_report_progress_every_250_messages_and_at_completion())


async def _report_progress_every_250_messages_and_at_completion() -> None:
    message_date = datetime(2026, 1, 1, tzinfo=UTC)
    service = FakeService(
        [
            FakeMessage(index, message_date)
            for index in range(251)
        ]
    )
    scanner = TelegramScanner(service)
    channel = Channel(
        id=123,
        title="Movies",
        username=None,
        unread_count=0,
        is_channel=True,
        is_group=False,
    )
    progress_counts: list[int] = []

    await scanner.scan_channel(
        channel,
        progress_callback=lambda result: progress_counts.append(
            result.scanned_messages
        ),
    )

    assert service.requested_entity_id == 123
    assert progress_counts == [250, 251]
