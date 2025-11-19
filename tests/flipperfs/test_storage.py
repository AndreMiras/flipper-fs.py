"""Test suite for flipperfs.storage module."""

from unittest.mock import MagicMock, patch
from flipperfs.storage import FlipperStorage


class TestFlipperStorage:
    """Test FlipperStorage class."""

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_list_files(self, mock_serial):
        mock_conn = MagicMock()
        mock_conn.is_open = True
        mock_conn.in_waiting = 100
        mock_serial.return_value = mock_conn

        # Mock the send_command response
        list_response = """[F] test1.sub 158b
[F] test2.sub 200b
[D] subdir
>:"""

        storage = FlipperStorage("/dev/test")
        with patch.object(storage.cli, "send_command", return_value=list_response):
            files = storage.list("/any/subghz")

        assert len(files) == 3
        assert files[0]["name"] == "test1.sub"
        assert files[0]["type"] == "file"
        assert files[0]["size"] == 158
        assert files[2]["type"] == "directory"

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_read_file(self, mock_serial):
        mock_conn = MagicMock()
        mock_conn.is_open = True
        mock_serial.return_value = mock_conn

        read_response = """Size: 50
Test content
Line 2
>:"""

        storage = FlipperStorage("/dev/test")
        with patch.object(storage.cli, "send_command", return_value=read_response):
            content = storage.read("/test.txt")

        assert "Test content" in content
        assert "Line 2" in content

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_stat_file(self, mock_serial):
        mock_conn = MagicMock()
        mock_conn.is_open = True
        mock_serial.return_value = mock_conn

        stat_response = "File, size: 158b"

        storage = FlipperStorage("/dev/test")
        with patch.object(storage.cli, "send_command", return_value=stat_response):
            stats = storage.stat("/test.sub")

        assert stats["type"] == "file"
        assert stats["size"] == 158

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_exists(self, mock_serial):
        mock_conn = MagicMock()
        mock_conn.is_open = True
        mock_serial.return_value = mock_conn

        storage = FlipperStorage("/dev/test")

        # Test file exists
        with patch.object(storage, "stat", return_value={"type": "file"}):
            assert storage.exists("/test.txt") is True

        # Test file doesn't exist
        with patch.object(storage, "stat", return_value=None):
            assert storage.exists("/nonexistent.txt") is False

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_context_manager(self, mock_serial):
        mock_conn = MagicMock()
        mock_conn.is_open = True
        mock_serial.return_value = mock_conn

        with FlipperStorage("/dev/test") as storage:
            assert storage is not None

        mock_conn.close.assert_called()
