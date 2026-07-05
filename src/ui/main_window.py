import asyncio

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from models import Channel, ScanResult
from telegram.scanner import TelegramScanner
from ui.widgets.channel_details_widget import ChannelDetailsWidget
from utils.logger import logger


class MainWindow(QMainWindow):
    def __init__(
            self,
            scanner: TelegramScanner,
    ):
        super().__init__()

        self._scanner = scanner

        self.setWindowTitle("Telegram Downloader")
        self.resize(1400, 850)

        self.setStatusBar(QStatusBar())

        self._all_channels: list[Channel] = []
        self._selected_channel_id: int | None = None
        self._scan_task: asyncio.Task | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)

        # ------------------------------------------------------------------
        # Toolbar
        # ------------------------------------------------------------------

        top = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search channels...")
        self.search.textChanged.connect(self._filter_channels)

        self.refresh_button = QPushButton("Reload Telegram")
        self.refresh_button.setEnabled(False)

        top.addWidget(self.search)
        top.addWidget(self.refresh_button)

        # ------------------------------------------------------------------
        # Body
        # ------------------------------------------------------------------

        body = QHBoxLayout()

        self.channels = QListWidget()
        self.channels.currentItemChanged.connect(
            self._on_current_item_changed
        )

        self.channel_header = QLabel("Channels (0)")
        self.channel_header.setObjectName("channelHeader")

        channels_column = QWidget()

        channels_layout = QVBoxLayout(channels_column)
        channels_layout.setContentsMargins(0, 0, 0, 0)

        channels_layout.addWidget(self.channel_header)
        channels_layout.addWidget(self.channels)

        self.details = ChannelDetailsWidget()
        self.details.scan_requested.connect(
            self._on_scan_requested
        )
        self.details.clear()

        body.addWidget(channels_column, 1)
        body.addWidget(self.details, 3)

        root.addLayout(top)
        root.addLayout(body, 1)

        self.search.setFocus()

        self.statusBar().showMessage("Ready")

    # ------------------------------------------------------------------

    def load_channels(
            self,
            channels: list[Channel],
    ) -> None:

        self._all_channels = list(channels)

        self._filter_channels()

        self.statusBar().showMessage(
            f"Connected | {len(channels)} Channels"
        )

    # ------------------------------------------------------------------

    def _filter_channels(self) -> None:

        query = self.search.text().strip().lower()

        self.channels.setUpdatesEnabled(False)

        self.channels.clear()

        selected_item: QListWidgetItem | None = None

        for channel in self._all_channels:

            if query and query not in channel.display_name.lower():
                continue

            item = QListWidgetItem(channel.display_name)
            item.setData(
                Qt.ItemDataRole.UserRole,
                channel,
            )

            self.channels.addItem(item)

            if channel.id == self._selected_channel_id:
                selected_item = item

        self.channels.setUpdatesEnabled(True)

        self.channel_header.setText(
            f"Channels ({self.channels.count()})"
        )

        if selected_item is not None:
            self.channels.setCurrentItem(selected_item)

        elif self.channels.count() > 0:
            self.channels.setCurrentRow(0)

    # ------------------------------------------------------------------

    def _on_current_item_changed(
            self,
            item: QListWidgetItem | None,
    ) -> None:

        if item is None:
            self._selected_channel_id = None
            self.details.clear()
            return

        channel = item.data(Qt.ItemDataRole.UserRole)

        if isinstance(channel, Channel):
            self._select_channel(channel)

    # ------------------------------------------------------------------

    async def _scan_channel(
            self,
            channel: Channel,
    ) -> None:

        logger.info("Starting scan of %s", channel.title)
        self.details.set_scanning(True)
        self.statusBar().showMessage(
            f"Scanning {channel.title}..."
        )

        try:
            result = await self._scanner.scan_channel(
                channel,
                progress_callback=self._on_scan_progress,
            )

        except Exception:
            logger.exception(
                "Scan failed for %s",
                channel.title,
            )
            self.statusBar().showMessage(
                f"Scan failed: {channel.title}"
            )

        else:
            logger.info(
                "Scan completed: %s",
                result,
            )

            if self._selected_channel_id == channel.id:
                self.details.set_scan_result(result)

            self.statusBar().showMessage(
                f"Scan completed | {result.total_files} files | "
                f"{result.human_size}"
            )

        finally:
            self.details.set_scanning(False)

            if self._scan_task is asyncio.current_task():
                self._scan_task = None

    # ------------------------------------------------------------------

    def _on_scan_requested(
            self,
            channel: Channel,
    ) -> None:

        if self._scan_task is not None and not self._scan_task.done():
            self.statusBar().showMessage(
                "A scan is already running"
            )
            return

        self._scan_task = asyncio.create_task(
            self._scan_channel(channel)
        )

    # ------------------------------------------------------------------

    def _on_scan_progress(
            self,
            result: ScanResult,
    ) -> None:

        if self._selected_channel_id == result.channel_id:
            self.details.set_scan_result(result)

        self.statusBar().showMessage(
            f"Scanning {result.channel_name} | "
            f"{result.scanned_messages} messages | "
            f"{result.total_files} files | "
            f"{result.human_size}"
        )

    # ------------------------------------------------------------------

    def _select_channel(
            self,
            channel: Channel,
    ) -> None:

        self._selected_channel_id = channel.id

        self.details.set_channel(channel)

        if self._scan_task is not None and not self._scan_task.done():
            self.details.set_scanning(True)
