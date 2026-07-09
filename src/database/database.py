"""
Database connection management.

This module owns the SQLite connection lifecycle.
Repositories must NEVER call sqlite3.connect() directly.

Responsibilities:
    - Open database connections
    - Configure SQLite PRAGMAs
    - Return shared connection
    - Close connection
"""

from __future__ import annotations

import sqlite3
from threading import RLock

from database.config import (
    BUSY_TIMEOUT_MS,
    DATABASE_PATH,
    ENABLE_FOREIGN_KEYS,
    ENABLE_WAL,
    SYNCHRONOUS_MODE,
    TEMP_STORE,
)
from database.exceptions import DatabaseConnectionError


class Database:
    """
    Singleton-style database connection manager.
    """

    _connection: sqlite3.Connection | None = None
    _lock = RLock()

    @classmethod
    def connect(cls) -> sqlite3.Connection:
        """
        Return an initialized SQLite connection.

        Creates the connection on first access.
        """

        with cls._lock:

            if cls._connection is not None:
                return cls._connection

            try:
                DATABASE_PATH.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                connection = sqlite3.connect(
                    DATABASE_PATH,
                    check_same_thread=False,
                )

                connection.row_factory = sqlite3.Row

                cls._configure(connection)

                cls._connection = connection

                return connection

            except sqlite3.Error as exc:
                raise DatabaseConnectionError(
                    f"Unable to connect to database: {exc}"
                ) from exc

    @classmethod
    def _configure(
            cls,
            connection: sqlite3.Connection,
    ) -> None:
        """
        Configure SQLite connection.
        """

        cursor = connection.cursor()

        if ENABLE_FOREIGN_KEYS:
            cursor.execute(
                "PRAGMA foreign_keys = ON;"
            )

        if ENABLE_WAL:
            cursor.execute(
                "PRAGMA journal_mode = WAL;"
            )

        cursor.execute(
            f"PRAGMA busy_timeout = {BUSY_TIMEOUT_MS};"
        )

        cursor.execute(
            f"PRAGMA synchronous = {SYNCHRONOUS_MODE};"
        )

        cursor.execute(
            f"PRAGMA temp_store = {TEMP_STORE};"
        )

        cursor.close()

    @classmethod
    def close(cls) -> None:
        """
        Close the shared connection.
        """

        with cls._lock:
            if cls._connection is None:
                return

            cls._connection.close()
            cls._connection = None


def get_connection() -> sqlite3.Connection:
    """
    Convenience helper.

    Example:
        conn = get_connection()
    """

    return Database.connect()
