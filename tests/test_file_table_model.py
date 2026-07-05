from datetime import UTC, datetime

from PySide6.QtCore import Qt

from models import FileInfo
from ui.models import FileTableModel


def make_file(
        file_name: str,
        category: str,
        extension: str,
        size: int,
        date: datetime,
) -> FileInfo:
    return FileInfo(
        message_id=1,
        file_name=file_name,
        category=category,
        extension=extension,
        size=size,
        date=date,
        mime_type=None,
        channel_id=123,
    )


def test_file_table_model_exposes_file_rows() -> None:
    file_info = make_file(
        "Docker.zip",
        "archives",
        ".zip",
        1536,
        datetime(2025, 3, 15, tzinfo=UTC),
    )
    model = FileTableModel([file_info])

    assert model.rowCount() == 1
    assert model.columnCount() == 5
    assert model.headerData(
        0,
        Qt.Orientation.Horizontal,
    ) == "Name"
    assert model.data(model.index(0, 0)) == "Docker.zip"
    assert model.data(model.index(0, 1)) == "Archive"
    assert model.data(model.index(0, 2)) == ".zip"
    assert model.data(model.index(0, 3)) == "1.50 KB"
    assert model.data(model.index(0, 4)) == "15-Mar-2025"
    assert model.data(
        model.index(0, 0),
        Qt.ItemDataRole.UserRole,
    ) == file_info


def test_file_table_model_loads_files() -> None:
    model = FileTableModel()

    model.load_files(
        [
            make_file(
                "Intro.mp4",
                "videos",
                ".mp4",
                700,
                datetime(2025, 3, 15, tzinfo=UTC),
            )
        ]
    )

    assert model.rowCount() == 1
    assert model.data(model.index(0, 1)) == "Video"


def test_empty_model() -> None:
    model = FileTableModel()

    assert model.rowCount() == 0


def test_file_table_model_sorts_by_name_and_size() -> None:
    large_file = make_file(
        "Intro.mp4",
        "videos",
        ".mp4",
        2_000,
        datetime(2025, 3, 16, tzinfo=UTC),
    )
    small_file = make_file(
        "Docker.zip",
        "archives",
        ".zip",
        1_000,
        datetime(2025, 3, 15, tzinfo=UTC),
    )
    model = FileTableModel([large_file, small_file])

    model.sort(
        0,
        Qt.SortOrder.AscendingOrder,
    )

    assert model.file_at(0) == small_file

    model.sort(
        3,
        Qt.SortOrder.DescendingOrder,
    )

    assert model.file_at(0) == large_file
