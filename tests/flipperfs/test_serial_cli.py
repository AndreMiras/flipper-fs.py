"""Test suite for flipperfs.serial_cli module."""

from unittest.mock import MagicMock, patch
from flipperfs.serial_cli import SerialCLI


class TestSerialCLI:
    """Test SerialCLI class."""

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_connect(self, mock_serial):
        mock_conn = MagicMock()
        mock_serial.return_value = mock_conn

        cli = SerialCLI("/dev/test")
        assert cli.port == "/dev/test"
        assert cli.baud_rate == 230400
        mock_serial.assert_called_once()

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_send_command(self, mock_serial):
        mock_conn = MagicMock()
        mock_conn.is_open = True
        mock_conn.in_waiting = 10
        mock_conn.read.return_value = b"response>:"
        mock_serial.return_value = mock_conn

        cli = SerialCLI("/dev/test")
        response = cli.send_command("test command")

        assert "response" in response
        mock_conn.write.assert_called()
