import asyncio
from dataclasses import dataclass

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
    messages = [
        FakeMessage(),
        FakeMessage(FakeFile("clip.mp4", ".mp4", 100)),
        FakeMessage(FakeFile("book.pdf", ".pdf", 200)),
        FakeMessage(FakeFile(None, ".jpg", 300)),
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


def test_scanner_reports_progress_every_250_messages_and_at_completion() -> None:
    asyncio.run(_report_progress_every_250_messages_and_at_completion())


async def _report_progress_every_250_messages_and_at_completion() -> None:
    service = FakeService(
        [FakeMessage() for _ in range(251)]
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
