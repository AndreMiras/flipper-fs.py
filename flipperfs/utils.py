"""Utility functions for Flipper filesystem operations."""

import re


def normalize_path(path: str) -> str:
    """Normalize Flipper filesystem path."""
    # Ensure path starts with /
    if not path.startswith("/"):
        path = "/" + path

    # Remove duplicate slashes
    path = re.sub(r"/+", "/", path)

    # Remove trailing slash except for root
    if path != "/" and path.endswith("/"):
        path = path[:-1]

    return path


def parse_size(size_str: str) -> int:
    """Parse size string like '158b' to integer bytes."""
    if size_str.endswith("b"):
        return int(size_str[:-1])
    elif size_str.endswith("KiB"):
        return int(float(size_str[:-3]) * 1024)
    elif size_str.endswith("MiB"):
        return int(float(size_str[:-3]) * 1024 * 1024)
    else:
        return int(size_str)


def format_sub_key(hex_key: str) -> str:
    """Format hex key for .sub file (add spaces)."""
    # Remove any existing spaces
    hex_key = hex_key.replace(" ", "")

    # Add space every 2 characters
    return " ".join([hex_key[i : i + 2] for i in range(0, len(hex_key), 2)])


def create_sub_content(
    hex_key: str,
    frequency: int = 433920000,
    protocol: str = "Dooya",
    preset: str = "FuriHalSubGhzPresetOok650Async",
    bit_length: int = 40,
) -> str:
    """Create .sub file content from parameters."""
    formatted_key = format_sub_key(hex_key)

    return f"""Filetype: Flipper SubGhz Key File
Version: 1
Frequency: {frequency}
Preset: {preset}
Protocol: {protocol}
Bit: {bit_length}
Key: {formatted_key}"""
