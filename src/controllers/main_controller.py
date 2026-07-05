from telegram.repository import TelegramRepository


class MainController:

    def __init__(
            self,
            repository: TelegramRepository,
    ):
        self.repository = repository

    async def get_channels(self):
        return await self.repository.get_channels()
