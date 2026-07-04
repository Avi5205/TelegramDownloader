#!/bin/bash

set -e

echo "🚀 TGVault Sprint 3"

mkdir -p src/controllers
mkdir -p src/telegram
mkdir -p src/ui/widgets
mkdir -p src/config
mkdir -p src/database
mkdir -p src/services
mkdir -p src/models
mkdir -p src/utils
mkdir -p logs

touch src/controllers/__init__.py
touch src/ui/widgets/__init__.py

####################################################################################
# Controller
####################################################################################

cat > src/controllers/main_controller.py <<'EOF'
from telegram.repository import TelegramRepository


class MainController:

    def __init__(self):
        self.repository = TelegramRepository()

    async def get_channels(self):
        return await self.repository.get_channels()
EOF

####################################################################################
# Repository
####################################################################################

cat > src/telegram/repository.py <<'EOF'
class TelegramRepository:

    def __init__(self):
        pass

    async def get_channels(self):
        return []
EOF

####################################################################################
# Main Window
####################################################################################

cat > src/ui/main_window.py <<'EOF'
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
EOF

####################################################################################
# Main
####################################################################################

cat > src/main.py <<'EOF'
import asyncio
import sys

from PySide6.QtWidgets import QApplication

from telegram.client import TelegramService
from ui.main_window import MainWindow


async def startup():

    telegram = TelegramService()

    await telegram.connect()

    me = await telegram.me()

    print(f"Logged in as {me.first_name}")

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    app.exec()

    await telegram.disconnect()


if __name__ == "__main__":
    asyncio.run(startup())
EOF

echo "✅ Sprint 3 completed."
echo ""
echo "Run:"
echo ""
echo "python src/main.py"