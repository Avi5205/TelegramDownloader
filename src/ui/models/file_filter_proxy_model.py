import sys
from typing import Optional, Tuple, Final

from PySide6.QtCore import QSortFilterProxyModel, Qt, QModelIndex

MAX_SIZE: Final[int] = sys.maxsize


class FileFilterProxyModel(QSortFilterProxyModel):
    """Proxy model that provides searching and category filtering for FileTableModel.

    It expects the source model to return the FileInfo dataclass instance for
    Qt.UserRole on each row (FileTableModel does this).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._search_text: str = ""
        self._category: Optional[str] = None
        self._size_range: Optional[Tuple[int, int]] = None  # (min_bytes, max_bytes)

    # ------------------------- Public API ---------------------------------
    def set_search_text(self, text: str) -> None:
        self._search_text = (text or "").strip().lower()
        self.invalidateFilter()

    def set_category_filter(self, category: Optional[str]) -> None:
        """Set a category filter (e.g. 'videos', 'images').

        Pass None to clear the category filter.
        """
        self._category = category
        self.invalidateFilter()

    def set_size_range(self, min_bytes: Optional[int], max_bytes: Optional[int]) -> None:
        """Set size range filter in bytes. Use None to indicate open-ended bounds."""
        if min_bytes is None and max_bytes is None:
            self._size_range = None
        else:
            self._size_range = (
                0 if min_bytes is None else int(min_bytes),
                MAX_SIZE if max_bytes is None else int(max_bytes),
            )
        self.invalidateFilter()

    def clear_filters(self) -> None:
        self._search_text = ""
        self._category = None
        self._size_range = None
        self.invalidateFilter()

    # ------------------------- Filtering ---------------------------------
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        model = self.sourceModel()
        if model is None:
            return True

        # Retrieve the FileInfo object from the source model using UserRole.
        idx = model.index(source_row, 0, source_parent)
        file_info = model.data(idx, Qt.ItemDataRole.UserRole)

        if file_info is None:
            # If the source model doesn't provide FileInfo, fall back to default behaviour.
            return super().filterAcceptsRow(source_row, source_parent)

        return (
                self._matches_category(file_info)
                and self._matches_size(file_info)
                and self._matches_search(file_info)
        )

    # ------------------------- Match helpers ---------------------------------
    def _matches_category(self, file_info) -> bool:
        if self._category is None:
            return True

        return file_info.category == self._category

    def _matches_size(self, file_info) -> bool:
        if self._size_range is None:
            return True

        min_b, max_b = self._size_range
        size = file_info.size
        return min_b <= size <= max_b

    def _matches_search(self, file_info) -> bool:
        if not self._search_text:
            return True

        # Search across fields likely to be useful: name, extension, category, mime_type
        parts = [
            file_info.file_name or "",
            (file_info.extension or ""),
            (file_info.category or ""),
            (file_info.mime_type or ""),
        ]

        hay = " ".join(parts).lower()
        return self._search_text in hay

    # ------------------------- Convenience accessors -----------------------
    def search_text(self) -> str:
        return self._search_text

    def category_filter(self) -> Optional[str]:
        return self._category

    def size_range(self) -> Optional[Tuple[int, int]]:
        return self._size_range
