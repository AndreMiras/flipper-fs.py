"""FlipperFS - Flipper Zero Filesystem Operations via Serial CLI.

A Python library for reliable filesystem operations on Flipper Zero devices
using direct serial communication at 230400 baud.

This package is published on PyPI as 'flipper-fs'. Install with:
    pip install flipper-fs

Import as:
    import flipperfs
"""

from .serial_cli import SerialCLI
from .storage import FlipperStorage
from .exceptions import (
    FlipperFilesystemError,
    ConnectionError,
    FileNotFoundError,
    WriteError,
    ReadError
)

# Version is managed by setuptools-scm from git tags
try:
    from importlib.metadata import version
    __version__ = version("flipper-fs")
except Exception:
    # Fallback for development environments without proper installation
    __version__ = "unknown"
__author__ = "Andre Miras"
__license__ = "MIT"

__all__ = [
    "SerialCLI",
    "FlipperStorage",
    "FlipperFilesystemError",
    "ConnectionError",
    "FileNotFoundError",
    "WriteError",
    "ReadError"
]

# Optional Sub-GHz module
try:
    from .extras.subghz import SubGhzStorage
    __all__.append("SubGhzStorage")
except ImportError:
    SubGhzStorage = None
