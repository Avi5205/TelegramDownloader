from models.scan_result import ScanResult


def test_scan_result_defaults() -> None:
    result = ScanResult(
        channel_id=123,
        channel_name="Example",
    )

    assert result.channel_id == 123
    assert result.channel_name == "Example"
    assert result.total_messages == 0
    assert result.scanned_messages == 0
    assert result.total_files == 0
    assert result.started_at is not None
    assert result.completed_at is None
    assert result.completed is False


def test_scan_result_calculates_size_mb() -> None:
    result = ScanResult(
        channel_id=123,
        channel_name="Example",
        total_size=2 * 1024 * 1024,
    )

    assert result.size_mb == 2.0


def test_scan_result_formats_human_size() -> None:
    result = ScanResult(
        channel_id=123,
        channel_name="Example",
        total_size=1536,
    )

    assert result.human_size == "1.50 KB"


def test_scan_result_returns_zero_duration_until_completed() -> None:
    result = ScanResult(
        channel_id=123,
        channel_name="Example",
    )

    assert result.duration_seconds == 0.0
