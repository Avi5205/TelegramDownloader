from collections.abc import Iterable

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from models import FileInfo


class FileTableModel(QAbstractTableModel):
    """
    Table model that exposes scanned Telegram files to Qt views.
    """

    HEADERS = (
        "Name",
        "Category",
        "Extension",
        "Size",
        "Date",
    )

    def __init__(
        self,
        files: Iterable[FileInfo] | None = None,
        parent=None,
    ):
        super().__init__(parent)

        self._files = list(files or [])

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

        return len(self.HEADERS)

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
            return self._display_value(file_info, index.column())

        if role == Qt.ItemDataRole.UserRole:
            return file_info

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return self._alignment(index.column())

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
            if 0 <= section < len(self.HEADERS):
                return self.HEADERS[section]

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

    def sort(
        self,
        column: int,
        order: Qt.SortOrder = Qt.SortOrder.AscendingOrder,
    ) -> None:
        if not 0 <= column < len(self.HEADERS):
            return

        self.layoutAboutToBeChanged.emit()
        self._files.sort(
            key=lambda file_info: self._sort_value(file_info, column),
            reverse=order == Qt.SortOrder.DescendingOrder,
        )
        self.layoutChanged.emit()

    def load_files(
        self,
        files: Iterable[FileInfo],
    ) -> None:
        self.beginResetModel()
        self._files = list(files)
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

    def _display_value(
        self,
        file_info: FileInfo,
        column: int,
    ) -> str:
        if column == 0:
            return file_info.file_name

        if column == 1:
            return self._display_category(file_info.category)

        if column == 2:
            return file_info.extension or "-"

        if column == 3:
            return file_info.human_size

        if column == 4:
            return file_info.date.strftime("%d-%b-%Y")

        return ""

    def _sort_value(
        self,
        file_info: FileInfo,
        column: int,
    ):
        if column == 0:
            return file_info.file_name.lower()

        if column == 1:
            return self._display_category(file_info.category).lower()

        if column == 2:
            return file_info.extension.lower()

        if column == 3:
            return file_info.size

        if column == 4:
            return file_info.date

        return ""

    def _alignment(
        self,
        column: int,
    ) -> Qt.AlignmentFlag:
        if column == 3:
            return (
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

        if column == 4:
            return (
                Qt.AlignmentFlag.AlignCenter
                | Qt.AlignmentFlag.AlignVCenter
            )

        return (
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

    def _display_category(
        self,
        category: str,
    ) -> str:
        labels = {
            "videos": "Video",
            "documents": "Document",
            "images": "Image",
            "audio": "Audio",
            "archives": "Archive",
            "others": "Other",
        }

        return labels.get(category, category.title())
