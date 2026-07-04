from telethon.tl.types import Channel as TelegramChannel
from telethon.tl.types import Chat

from models import Channel
from telegram.client import TelegramService


class TelegramRepository:

    def __init__(self, service: TelegramService):
        self._service = service

    async def get_channels(self) -> list[Channel]:
        """
        Returns all Telegram Channels and Groups.
        """

        channels: list[Channel] = []

        async for dialog in self._service.iter_dialogs():

            entity = dialog.entity

            if isinstance(entity, TelegramChannel):

                channels.append(
                    Channel(
                        id=entity.id,
                        title=entity.title,
                        username=entity.username,
                        unread_count=dialog.unread_count,
                        is_channel=entity.broadcast,
                        is_group=entity.megagroup,
                    )
                )

            elif isinstance(entity, Chat):

                channels.append(
                    Channel(
                        id=entity.id,
                        title=entity.title,
                        username=None,
                        unread_count=dialog.unread_count,
                        is_channel=False,
                        is_group=True,
                    )
                )

        channels.sort(key=lambda c: c.title.lower())

        return channels
