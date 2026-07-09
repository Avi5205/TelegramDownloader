from database.database import get_connection
from models import Channel


class ChannelRepository:
    def save_channels(self, channels: list[Channel]) -> None:
        conn = get_connection()
        cur = conn.cursor()
        rows = [
            (c.id, c.title, c.username)
            for c in channels
        ]
        cur.executemany(
            """
            INSERT OR REPLACE INTO channels (id, title, username)
            VALUES (?, ?, ?)
            """,
            rows,
        )
        conn.commit()
        conn.close()

    def get_channels(self) -> list[Channel]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, username FROM channels")
        rows = cur.fetchall()
        conn.close()

        return [
            Channel(
                id=row["id"],
                title=row["title"],
                username=row["username"],
            )
            for row in rows
        ]
