from telethon import TelegramClient

from config.paths import SESSIONS_DIR
from config.settings import (
    API_ID,
    API_HASH,
    SESSION_NAME,
)


class TelegramService:

    def __init__(self):
        session_path = SESSIONS_DIR / SESSION_NAME

        self._client = TelegramClient(
            str(session_path),
            API_ID,
            API_HASH,
        )

    async def connect(self):

        await self._client.start()

    async def disconnect(self):

        await self._client.disconnect()

    async def me(self):

        return await self._client.get_me()

    async def iter_dialogs(self):

        async for dialog in self._client.iter_dialogs():
            yield dialog

    async def iter_messages(self, entity):

        async for message in self._client.iter_messages(entity):
            yield message

    async def get_entity(self, entity_id):

        return await self._client.get_entity(entity_id)
