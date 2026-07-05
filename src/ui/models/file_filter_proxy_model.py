from typing import Optional, Tuple

from PySide6.QtCore import QSortFilterProxyModel, Qt, QModelIndex


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
                2 ** 63 - 1 if max_bytes is None else int(max_bytes),
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

        # Category filter
        if self._category:
            if getattr(file_info, "category", None) != self._category:
                return False

        # Size range filter
        if self._size_range is not None:
            min_b, max_b = self._size_range
            size = getattr(file_info, "size", 0)
            if size < min_b or size > max_b:
                return False

        # Search text filter (applied to name, extension, and category)
        if self._search_text:
            hay = " ".join(
                [
                    str(getattr(file_info, "file_name", "")),
                    str(getattr(file_info, "extension", "") or ""),
                    str(getattr(file_info, "category", "") or ""),
                ]
            ).lower()

            if self._search_text not in hay:
                return False

        return True

    # Optional: expose convenient properties
    def search_text(self) -> str:
        return self._search_text

    def category_filter(self) -> Optional[str]:
        return self._category

    def size_range(self) -> Optional[Tuple[int, int]]:
        return self._size_range
