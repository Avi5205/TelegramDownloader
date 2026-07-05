from dataclasses import dataclass


@dataclass(slots=True)
class Channel:
    """
    Represents a Telegram Channel or Group.
    This model is independent of Telethon.
    """

    id: int
    title: str
    username: str | None
    unread_count: int
    is_channel: bool
    is_group: bool

    @property
    def display_name(self) -> str:
        """Text displayed in the UI."""
        return self.title
