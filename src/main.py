import asyncio
import sys

from PySide6.QtWidgets import QApplication

from telegram.client import TelegramService
from telegram.repository import TelegramRepository
from ui.main_window import MainWindow


async def startup():

    telegram = TelegramService()
    await telegram.connect()

    me = await telegram.me()
    print(f"Logged in as {me.first_name}")

    repository = TelegramRepository(telegram)
    channels = await repository.get_channels()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.load_channels(channels)

    window.show()

    app.exec()

    await telegram.disconnect()


if __name__ == "__main__":
    asyncio.run(startup())