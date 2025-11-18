"""Custom exceptions for Flipper filesystem operations."""


class FlipperFilesystemError(Exception):
    """Base exception for all filesystem operations."""
    pass


class ConnectionError(FlipperFilesystemError):
    """Failed to connect or communicate with Flipper."""
    pass


class FileNotFoundError(FlipperFilesystemError):
    """File or directory not found on Flipper."""
    pass


class WriteError(FlipperFilesystemError):
    """Failed to write file to Flipper."""
    pass


class ReadError(FlipperFilesystemError):
    """Failed to read file from Flipper."""
    pass
