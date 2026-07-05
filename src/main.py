import asyncio
import sys

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from download.manager import DownloadManager
from telegram.client import TelegramService
from telegram.repository import TelegramRepository
from telegram.scanner import TelegramScanner
from ui.main_window import MainWindow
from utils.logger import logger


async def initialize(
        window: MainWindow,
        telegram: TelegramService,
        repository: TelegramRepository,
) -> None:
    await telegram.connect()

    me = await telegram.me()

    logger.info("Connected as %s", me.first_name)

    channels = await repository.get_channels()

    window.load_channels(channels)


def main() -> None:
    app = QApplication(sys.argv)

    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)

    telegram = TelegramService()

    repository = TelegramRepository(telegram)
    scanner = TelegramScanner(telegram)
    download_manager = DownloadManager(telegram)

    window = MainWindow(scanner, download_manager)
    window.show()

    with loop:
        loop.create_task(
            initialize(window, telegram, repository)
        )
        loop.run_forever()


if __name__ == "__main__":
    main()
