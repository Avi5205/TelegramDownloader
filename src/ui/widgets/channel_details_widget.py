from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from models import Channel, ScanResult

EMPTY_VALUE = "-"


class ChannelDetailsWidget(QWidget):
    scan_requested = Signal(object)

    def __init__(self):
        super().__init__()

        self._channel: Channel | None = None

        self._build_ui()

    # ------------------------------------------------------------------

    def _build_ui(self) -> None:

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Channel Information")
        title.setObjectName("detailsTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(title)

        group = QGroupBox()

        form = QFormLayout(group)
        form.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.name_value = self._create_value_label()
        self.username_value = self._create_value_label()
        self.type_value = self._create_value_label()
        self.unread_value = self._create_value_label()
        self.id_value = self._create_value_label()

        form.addRow("Name", self.name_value)
        form.addRow("Username", self.username_value)
        form.addRow("Type", self.type_value)
        form.addRow("Unread", self.unread_value)
        form.addRow("ID", self.id_value)

        layout.addWidget(group)

        summary_title = QLabel("Scan Summary")
        summary_title.setObjectName("detailsTitle")
        summary_title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(summary_title)

        summary_group = QGroupBox()

        summary_form = QFormLayout(summary_group)
        summary_form.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.messages_value = self._create_value_label()
        self.files_value = self._create_value_label()
        self.videos_value = self._create_value_label()
        self.documents_value = self._create_value_label()
        self.images_value = self._create_value_label()
        self.archives_value = self._create_value_label()
        self.total_size_value = self._create_value_label()
        self.duration_value = self._create_value_label()

        summary_form.addRow("Messages", self.messages_value)
        summary_form.addRow("Files", self.files_value)
        summary_form.addRow("Videos", self.videos_value)
        summary_form.addRow("Documents", self.documents_value)
        summary_form.addRow("Images", self.images_value)
        summary_form.addRow("Archives", self.archives_value)
        summary_form.addRow("Total Size", self.total_size_value)
        summary_form.addRow("Duration", self.duration_value)

        layout.addWidget(summary_group)

        self.scan_button = QPushButton("Scan Channel")
        self.scan_button.setEnabled(False)
        self.scan_button.clicked.connect(self._request_scan)

        self.scan_progress = QProgressBar()
        self.scan_progress.setTextVisible(False)
        self.scan_progress.setRange(0, 1)
        self.scan_progress.setValue(0)
        self.scan_progress.setVisible(False)

        layout.addWidget(self.scan_progress)
        layout.addWidget(self.scan_button)
        layout.addStretch()

    # ------------------------------------------------------------------

    def _create_value_label(self) -> QLabel:

        label = QLabel(EMPTY_VALUE)

        label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        return label

    # ------------------------------------------------------------------

    def clear(self) -> None:
        self._channel = None

        self.name_value.setText(EMPTY_VALUE)
        self.username_value.setText(EMPTY_VALUE)
        self.type_value.setText(EMPTY_VALUE)
        self.unread_value.setText(EMPTY_VALUE)
        self.id_value.setText(EMPTY_VALUE)

        self.clear_scan_result()
        self.scan_button.setEnabled(False)
        self.scan_button.setText("Scan Channel")
        self.scan_progress.setRange(0, 1)
        self.scan_progress.setValue(0)
        self.scan_progress.setVisible(False)

    # ------------------------------------------------------------------

    def set_channel(
        self,
        channel: Channel | None,
    ) -> None:

        if channel is None:
            self.clear()
            return

        self._channel = channel

        self.name_value.setText(channel.title)

        self.username_value.setText(
            channel.username or EMPTY_VALUE
        )

        self.type_value.setText(
            "Channel"
            if channel.is_channel
            else "Group"
        )

        self.unread_value.setText(
            str(channel.unread_count)
        )

        self.id_value.setText(
            str(channel.id)
        )

        self.clear_scan_result()
        self.scan_button.setEnabled(True)
        self.scan_button.setText("Scan Channel")
        self.scan_progress.setRange(0, 1)
        self.scan_progress.setValue(0)
        self.scan_progress.setVisible(False)

    # ------------------------------------------------------------------

    def clear_scan_result(self) -> None:

        self.messages_value.setText(EMPTY_VALUE)
        self.files_value.setText(EMPTY_VALUE)
        self.videos_value.setText(EMPTY_VALUE)
        self.documents_value.setText(EMPTY_VALUE)
        self.images_value.setText(EMPTY_VALUE)
        self.archives_value.setText(EMPTY_VALUE)
        self.total_size_value.setText(EMPTY_VALUE)
        self.duration_value.setText(EMPTY_VALUE)

    # ------------------------------------------------------------------

    def set_scan_result(
        self,
        result: ScanResult,
    ) -> None:

        self.messages_value.setText(str(result.scanned_messages))
        self.files_value.setText(str(result.total_files))
        self.videos_value.setText(str(result.videos))
        self.documents_value.setText(str(result.documents))
        self.images_value.setText(str(result.images))
        self.archives_value.setText(str(result.archives))
        self.total_size_value.setText(result.human_size)
        self.duration_value.setText(
            f"{result.duration_seconds:.2f} s"
        )

    # ------------------------------------------------------------------

    def set_scanning(
        self,
        scanning: bool,
    ) -> None:

        self.scan_button.setEnabled(
            not scanning and self._channel is not None
        )
        self.scan_button.setText(
            "Scanning..." if scanning else "Scan Channel"
        )
        self.scan_progress.setVisible(scanning)

        if scanning:
            self.scan_progress.setRange(0, 0)
        else:
            self.scan_progress.setRange(0, 1)
            self.scan_progress.setValue(1)

    # ------------------------------------------------------------------

    def _request_scan(self) -> None:

        if self._channel is not None and self.scan_button.isEnabled():
            self.scan_requested.emit(self._channel)
