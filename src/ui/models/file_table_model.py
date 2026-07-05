from collections.abc import Iterable
from enum import IntEnum
from typing import Final

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from models import FileInfo


class Columns(IntEnum):
    NAME = 0
    CATEGORY = 1
    EXTENSION = 2
    SIZE = 3
    DATE = 4


HEADERS: Final[tuple[str, ...]] = (
    "Name",
    "Category",
    "Extension",
    "Size",
    "Date",
)

CATEGORY_LABELS: Final[dict[str, str]] = {
    "videos": "Video",
    "documents": "Document",
    "images": "Image",
    "audio": "Audio",
    "archives": "Archive",
    "others": "Other",
}


class FileTableModel(QAbstractTableModel):
    """
    Table model exposing scanned Telegram files.
    """

    def __init__(
        self,
        files: Iterable[FileInfo] | None = None,
        parent=None,
    ):
        super().__init__(parent)

        self._files = list(files or [])

    # ------------------------------------------------------------------
    # Qt Model API
    # ------------------------------------------------------------------

    def rowCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        if parent.isValid():
            return 0

        return len(self._files)

    def columnCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        if parent.isValid():
            return 0

        return len(HEADERS)

    def data(
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if not index.isValid():
            return None

        file_info = self.file_at(index.row())

        if file_info is None:
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return self._display_value(
                file_info,
                Columns(index.column()),
            )

        if role == Qt.ItemDataRole.UserRole:
            return file_info

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return self._alignment(
                Columns(index.column())
            )

        # Future:
        # if role == Qt.ItemDataRole.DecorationRole:
        #     return self._icon(file_info)

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:

            if 0 <= section < len(HEADERS):
                return HEADERS[section]

            return None

        return section + 1

    def flags(
        self,
        index: QModelIndex,
    ) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        return (
            Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_files(
        self,
        files: Iterable[FileInfo],
    ) -> None:

        self.beginResetModel()

        self._files = list(files)

        self.endResetModel()

    def sort(
        self,
        column: int,
        order: Qt.SortOrder = Qt.SortOrder.AscendingOrder,
    ) -> None:

        if not 0 <= column < len(HEADERS):
            return

        self.beginResetModel()

        self._files.sort(
            key=lambda file_info: self._sort_value(
                file_info,
                Columns(column),
            ),
            reverse=(
                order == Qt.SortOrder.DescendingOrder
            ),
        )

        self.endResetModel()

    def file_at(
        self,
        row: int,
    ) -> FileInfo | None:

        if 0 <= row < len(self._files):
            return self._files[row]

        return None

    def files(self) -> list[FileInfo]:
        return list(self._files)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _display_value(
        self,
        file_info: FileInfo,
        column: Columns,
    ) -> str:

        if column == Columns.NAME:
            return file_info.file_name

        if column == Columns.CATEGORY:
            return self._display_category(
                file_info.category
            )

        if column == Columns.EXTENSION:
            return file_info.extension or "-"

        if column == Columns.SIZE:
            return file_info.human_size

        if column == Columns.DATE:
            return file_info.date.strftime(
                "%d-%b-%Y"
            )

        return ""

    def _sort_value(
        self,
        file_info: FileInfo,
        column: Columns,
    ):

        if column == Columns.NAME:
            return (
                file_info.file_name or ""
            ).lower()

        if column == Columns.CATEGORY:
            return self._display_category(
                file_info.category
            ).lower()

        if column == Columns.EXTENSION:
            return (
                file_info.extension or ""
            ).lower()

        if column == Columns.SIZE:
            return file_info.size

        if column == Columns.DATE:
            return file_info.date

        return ""

    def _alignment(
        self,
        column: Columns,
    ) -> Qt.AlignmentFlag:

        if column == Columns.SIZE:
            return (
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

        if column == Columns.DATE:
            return (
                Qt.AlignmentFlag.AlignCenter
                | Qt.AlignmentFlag.AlignVCenter
            )

        return (
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

    @staticmethod
    def _display_category(
        category: str,
    ) -> str:
        return CATEGORY_LABELS.get(
            category,
            category.title(),
        )