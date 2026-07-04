from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from models import Channel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Telegram Downloader")
        self.resize(1200, 800)

        self.setStatusBar(QStatusBar())

        self._build_ui()

    def _build_ui(self) -> None:
        """Create the application layout."""

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout()
        central.setLayout(root)

        # Top toolbar
        top = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search channels...")

        self.refresh_button = QPushButton("Refresh")

        top.addWidget(self.search)
        top.addWidget(self.refresh_button)

        # Main content
        body = QHBoxLayout()

        self.channels = QListWidget()

        self.details = QLabel("Select a channel")
        self.details.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body.addWidget(self.channels, 1)
        body.addWidget(self.details, 3)

        root.addLayout(top)
        root.addLayout(body)

        self.statusBar().showMessage("Ready")

    def load_channels(self, channels: list[Channel]) -> None:
        """Populate the channel list."""

        self.channels.clear()

        for channel in channels:
            self.channels.addItem(channel.display_name)

        self.statusBar().showMessage(
            f"{len(channels)} channels loaded"
        )