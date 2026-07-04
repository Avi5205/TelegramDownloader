import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models import Channel
from ui.main_window import MainWindow


def test_filter_preserves_selected_channel_when_still_visible():
    app = QApplication.instance() or QApplication([])
    window = MainWindow()

    channel = Channel(1, "Movies", "movies", 0, True, False)
    window.load_channels([channel])

    window.channels.setCurrentRow(0)
    window.search.setText("mov")

    selected_items = window.channels.selectedItems()

    assert len(selected_items) == 1
    assert selected_items[0].text() == "Movies"
