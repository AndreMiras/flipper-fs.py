"""Sub-GHz specific filesystem operations."""

from typing import Dict, List
from ..storage import FlipperStorage
from ..utils import create_sub_content


class SubGhzStorage(FlipperStorage):
    """Extended storage operations for Sub-GHz files."""

    DEFAULT_SUBGHZ_PATH = "/any/subghz"

    def list_signals(self, directory: str = None) -> List[str]:
        """List all .sub signal files."""
        directory = directory or self.DEFAULT_SUBGHZ_PATH
        entries = self.list(directory)

        signals = []
        for entry in entries:
            if entry["type"] == "file" and entry["name"].endswith(".sub"):
                signals.append(entry["path"])

        return signals

    def read_signal(self, signal_name: str) -> Dict[str, str]:
        """Read and parse .sub file content."""
        # Handle both full path and just filename
        if not signal_name.startswith("/"):
            signal_path = f"{self.DEFAULT_SUBGHZ_PATH}/{signal_name}"
        else:
            signal_path = signal_name

        content = self.read(signal_path)

        # Parse .sub file
        signal_data = {}
        for line in content.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                signal_data[key.strip()] = value.strip()

        return signal_data

    def write_signal(
        self,
        signal_name: str,
        hex_key: str,
        frequency: int = 433920000,
        protocol: str = "Dooya",
        preset: str = "FuriHalSubGhzPresetOok650Async",
        bit_length: int = 40,
    ) -> bool:
        """Create a new .sub signal file."""
        if not signal_name.endswith(".sub"):
            signal_name += ".sub"

        if not signal_name.startswith("/"):
            signal_path = f"{self.DEFAULT_SUBGHZ_PATH}/{signal_name}"
        else:
            signal_path = signal_name

        content = create_sub_content(
            hex_key=hex_key,
            frequency=frequency,
            protocol=protocol,
            preset=preset,
            bit_length=bit_length,
        )

        return self.write(signal_path, content)

    def create_temp_signal(self, hex_key: str, **kwargs) -> str:
        """Create temporary signal file and return path."""
        import time

        temp_name = f"_temp_{int(time.time())}.sub"
        temp_path = f"{self.DEFAULT_SUBGHZ_PATH}/{temp_name}"

        self.write_signal(temp_path, hex_key, **kwargs)
        return temp_path
