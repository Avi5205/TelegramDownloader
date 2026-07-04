from telegram.repository import TelegramRepository


class MainController:

    def __init__(self):
        self.repository = TelegramRepository()

    async def get_channels(self):
        return await self.repository.get_channels()
