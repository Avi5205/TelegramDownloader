import asyncio
import sys

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from telegram.client import TelegramService
from telegram.repository import TelegramRepository
from ui.main_window import MainWindow
from utils.logger import logger


async def initialize(window: MainWindow) -> None:
    telegram = TelegramService()

    await telegram.connect()

    me = await telegram.me()

    logger.info("Connected as %s", me.first_name)

    repository = TelegramRepository(telegram)

    channels = await repository.get_channels()

    window.load_channels(channels)


def main() -> None:

    app = QApplication(sys.argv)

    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.create_task(
            initialize(window)
        )
        loop.run_forever()


if __name__ == "__main__":
    main()