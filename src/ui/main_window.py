from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QStatusBar
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TGVault")
        self.resize(1200, 800)

        self.setStatusBar(QStatusBar())

        central = QWidget()

        self.setCentralWidget(central)

        root = QVBoxLayout()

        top = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search channels...")

        self.refresh = QPushButton("Refresh")

        top.addWidget(self.search)
        top.addWidget(self.refresh)

        body = QHBoxLayout()

        self.channels = QListWidget()

        self.details = QLabel(
            "Select a channel"
        )

        self.details.setAlignment(Qt.AlignCenter)

        body.addWidget(self.channels,1)
        body.addWidget(self.details,3)

        root.addLayout(top)
        root.addLayout(body)

        central.setLayout(root)

        self.statusBar().showMessage("Connected")
