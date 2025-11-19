"""Test suite for flipperfs.extras.subghz module."""

from unittest.mock import MagicMock, patch
from flipperfs.extras.subghz import SubGhzStorage


class TestSubGhzStorage:
    """Test SubGhzStorage class."""

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_list_signals(self, mock_serial):
        mock_conn = MagicMock()
        mock_conn.is_open = True
        mock_serial.return_value = mock_conn

        list_response = """[F] signal1.sub 158b
[F] signal2.sub 200b
[F] readme.txt 50b
[D] subdir
>:"""

        subghz = SubGhzStorage("/dev/test")
        with patch.object(subghz.cli, "send_command", return_value=list_response):
            signals = subghz.list_signals()

        # Should only return .sub files
        assert len(signals) == 2
        assert "/any/subghz/signal1.sub" in signals
        assert "/any/subghz/signal2.sub" in signals

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_read_signal(self, mock_serial):
        mock_conn = MagicMock()
        mock_conn.is_open = True
        mock_serial.return_value = mock_conn

        signal_content = """Filetype: Flipper SubGhz Key File
Version: 1
Frequency: 433920000
Protocol: Dooya
Key: 00 00 00 12 F6 CC 05 3C"""

        read_response = f"Size: 100\n{signal_content}\n>:"

        subghz = SubGhzStorage("/dev/test")
        with patch.object(subghz.cli, "send_command", return_value=read_response):
            signal_data = subghz.read_signal("test.sub")

        assert signal_data["Filetype"] == "Flipper SubGhz Key File"
        assert signal_data["Frequency"] == "433920000"
        assert signal_data["Protocol"] == "Dooya"

    @patch("flipperfs.serial_cli.serial.Serial")
    def test_write_signal(self, mock_serial):
        mock_conn = MagicMock()
        mock_conn.is_open = True
        mock_serial.return_value = mock_conn

        subghz = SubGhzStorage("/dev/test")

        with patch.object(subghz, "write", return_value=True) as mock_write:
            result = subghz.write_signal("test", "00000012F6CC053C", protocol="Dooya")

        assert result is True
        mock_write.assert_called_once()

        # Verify the path was constructed correctly
        call_args = mock_write.call_args
        assert call_args[0][0] == "/any/subghz/test.sub"

        # Verify content has correct format
        content = call_args[0][1]
        assert "Filetype: Flipper SubGhz Key File" in content
        assert "Key: 00 00 00 12 F6 CC 05 3C" in content
