import asyncio
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models import Channel, ScanResult
from ui.main_window import MainWindow


class FakeScanner:
    pass


class BlockingScanner:
    def __init__(self):
        self.calls = 0
        self.release = asyncio.Event()

    async def scan_channel(
        self,
        channel: Channel,
        progress_callback=None,
    ) -> ScanResult:
        self.calls += 1
        await self.release.wait()

        return ScanResult(
            channel_id=channel.id,
            channel_name=channel.title,
        )


def test_filter_preserves_selected_channel_when_still_visible():
    app = QApplication.instance() or QApplication([])
    window = MainWindow(
        FakeScanner(),
    )

    channel = Channel(1, "Movies", "movies", 0, True, False)
    window.load_channels([channel])

    window.channels.setCurrentRow(0)
    window.search.setText("mov")

    selected_items = window.channels.selectedItems()

    assert len(selected_items) == 1
    assert selected_items[0].text() == "Movies"


def test_scan_request_ignores_duplicates_while_scan_is_running():
    asyncio.run(_scan_request_ignores_duplicates())


async def _scan_request_ignores_duplicates() -> None:
    app = QApplication.instance() or QApplication([])
    scanner = BlockingScanner()
    window = MainWindow(scanner)
    channel = Channel(1, "Movies", "movies", 0, True, False)

    window._select_channel(channel)

    window._on_scan_requested(channel)
    window._on_scan_requested(channel)

    await asyncio.sleep(0)

    assert scanner.calls == 1
    assert window._scan_task is not None

    task = window._scan_task
    scanner.release.set()

    await task

    assert window._scan_task is None
