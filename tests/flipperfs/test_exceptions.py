"""Test suite for flipperfs.exceptions module."""

import pytest
from flipperfs.exceptions import (
    FlipperFilesystemError,
    ConnectionError,
    FileNotFoundError,
    WriteError,
    ReadError
)


class TestExceptions:
    """Test exception classes."""

    def test_flipper_filesystem_error(self):
        """Test base exception."""
        with pytest.raises(FlipperFilesystemError):
            raise FlipperFilesystemError("Test error")

    def test_connection_error(self):
        """Test connection error exception."""
        with pytest.raises(ConnectionError):
            raise ConnectionError("Connection failed")

    def test_file_not_found_error(self):
        """Test file not found exception."""
        with pytest.raises(FileNotFoundError):
            raise FileNotFoundError("File not found")

    def test_write_error(self):
        """Test write error exception."""
        with pytest.raises(WriteError):
            raise WriteError("Write failed")

    def test_read_error(self):
        """Test read error exception."""
        with pytest.raises(ReadError):
            raise ReadError("Read failed")