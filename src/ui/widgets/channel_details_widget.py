from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from models import Channel

EMPTY_VALUE = "-"


class ChannelDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()

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

        self.name_value.setText(EMPTY_VALUE)
        self.username_value.setText(EMPTY_VALUE)
        self.type_value.setText(EMPTY_VALUE)
        self.unread_value.setText(EMPTY_VALUE)
        self.id_value.setText(EMPTY_VALUE)

    # ------------------------------------------------------------------

    def set_channel(
        self,
        channel: Channel | None,
    ) -> None:

        if channel is None:
            self.clear()
            return

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