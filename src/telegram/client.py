from telethon import TelegramClient

from config.settings import (
    API_ID,
    API_HASH,
    SESSION_NAME,
)


class TelegramService:

    def __init__(self):

        self.client = TelegramClient(
            f"sessions/{SESSION_NAME}",
            API_ID,
            API_HASH,
        )

    async def connect(self):

        await self.client.start()

    async def disconnect(self):

        await self.client.disconnect()

    async def me(self):

        return await self.client.get_me()