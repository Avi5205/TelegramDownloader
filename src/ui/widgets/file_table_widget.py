from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QComboBox,
    QTableView,
    QLabel,
    QSizePolicy,
)

from models.file_category import CATEGORY_LABELS


class FileTableWidget(QWidget):
    """Composable file browser widget.

    The widget expects the caller to provide a concrete FileTableModel and
    a FileFilterProxyModel. The proxy will be wired to the model automatically.

    Responsibilities:
    - Own the QTableView
    - Provide a search box and category combo
    - Expose a small footer showing visible/total counts
    - Emit file_activated(FileInfo) on double-click
    """

    file_activated: Signal = Signal(object)

    def __init__(self, model, proxy, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._model = model
        self._proxy = proxy

        # Wire proxy -> model
        self._proxy.setSourceModel(self._model)

        self._build_ui()
        self._connect_signals()
        self._update_footer()

    # ---------------- UI construction ---------------------------------
    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(6)

        # Toolbar (search + category)
        toolbar = QHBoxLayout()

        self._search = QLineEdit()
        self._search.setPlaceholderText("Search files...")
        self._search.setClearButtonEnabled(True)

        self._category = QComboBox()
        self._category.addItem("All", None)

        # Add categories from shared labels
        for key, label in CATEGORY_LABELS.items():
            self._category.addItem(label, key)

        toolbar.addWidget(self._search)
        toolbar.addWidget(self._category)

        # Table view
        self._table = QTableView()
        self._table.setModel(self._proxy)
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        # Allow multiple selection for future download features
        self._table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self._table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self._table.setSortingEnabled(True)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Footer
        footer = QHBoxLayout()
        self._footer_label = QLabel()
        footer.addWidget(self._footer_label)
        footer.addStretch()

        root.addLayout(toolbar)
        root.addWidget(self._table, 1)
        root.addLayout(footer)

    # ---------------- Signals ------------------------------------------
    def _connect_signals(self) -> None:
        self._search.textChanged.connect(self._on_search_changed)
        self._category.currentIndexChanged.connect(self._on_category_changed)

        # Proxy changes affect visible rows
        self._proxy.modelReset.connect(self._update_footer)
        self._proxy.layoutChanged.connect(self._update_footer)

        # Selection changes
        sel_model = self._table.selectionModel()
        if sel_model is not None:
            sel_model.selectionChanged.connect(self._update_footer)

        # Activation
        self._table.doubleClicked.connect(self._on_activated)

    # ---------------- Public API --------------------------------------

    # ---------------- Event handlers ----------------------------------
    def _on_search_changed(self, text: str) -> None:
        # Delegate to proxy
        self._proxy.set_search_text(text)

    def _on_category_changed(self, index: int) -> None:
        category = self._category.itemData(index)
        self._proxy.set_category_filter(category)

    def _on_activated(self, proxy_index) -> None:
        # Map proxy index to source model index and retrieve FileInfo
        src_index = self._proxy.mapToSource(proxy_index)
        # Request FileInfo via UserRole from source model (column 0)
        idx = self._model.index(src_index.row(), 0)
        file_info = self._model.data(idx, Qt.ItemDataRole.UserRole)
        if file_info is not None:
            self.file_activated.emit(file_info)

    # ---------------- Helpers -----------------------------------------
    def _update_footer(self, *_) -> None:
        try:
            visible = self._proxy.rowCount()
            total = self._model.rowCount()
        except Exception:
            visible = 0
            total = 0

        selected = 0
        sel_model = self._table.selectionModel()
        if sel_model is not None:
            selected = len(sel_model.selectedRows())

        self._footer_label.setText(f"Showing {visible} of {total} files    Selected: {selected}")
