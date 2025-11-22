"""High-level storage operations for Flipper Zero filesystem."""

import re
import time
import logging
from typing import List, Dict, Optional, Union
from .serial_cli import SerialCLI
from .exceptions import FileNotFoundError, WriteError, FlipperFilesystemError


class FlipperStorage:
    """Flipper Zero filesystem operations via serial CLI."""

    def __init__(self, port: str = "/dev/ttyACM0", baud_rate: int = None):
        """Initialize storage operations."""
        self.cli = SerialCLI(port, baud_rate)
        self.logger = logging.getLogger(__name__)

    def info(self, path: str = "/any") -> Dict[str, str]:
        """Get filesystem information."""
        response = self.cli.send_command(f"storage info {path}")

        # Parse response
        info = {}
        for line in response.split("\n"):
            if ":" in line and not line.startswith(">"):
                key, value = line.split(":", 1)
                info[key.strip()] = value.strip()

        return info

    def list(self, path: str = "/any") -> List[Dict[str, Union[str, int]]]:
        """List files and directories."""
        response = self.cli.send_command(f"storage list {path}")

        entries = []
        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("[F]"):  # File
                parts = line.split()
                if len(parts) >= 3:
                    name = parts[1]
                    size_str = parts[2] if len(parts) > 2 else "0b"
                    size = int(size_str.rstrip("b"))
                    entries.append(
                        {
                            "type": "file",
                            "name": name,
                            "size": size,
                            "path": f"{path}/{name}",
                        }
                    )
            elif line.startswith("[D]"):  # Directory
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[1]
                    entries.append(
                        {"type": "directory", "name": name, "path": f"{path}/{name}"}
                    )

        return entries

    def read(self, file_path: str) -> str:
        """Read file content as string."""
        response = self.cli.send_command(f"storage read {file_path}", timeout=5)

        # Check if file exists
        if "Size:" not in response:
            raise FileNotFoundError(f"File not found: {file_path}")

        # Extract content after size line
        lines = response.split("\n")
        content_start = 0
        for i, line in enumerate(lines):
            if line.startswith("Size:"):
                content_start = i + 1
                break

        # Remove command echo and prompt from content
        content_lines = []
        for line in lines[content_start:]:
            if not line.startswith(">") and ">:" not in line:
                content_lines.append(line)

        return "\n".join(content_lines)

    def write(self, file_path: str, content: str) -> bool:
        """Write content to file."""
        self.logger.info(f"Writing to {file_path}")

        # Start write command
        self.cli.send_raw(f"storage write {file_path}\r".encode())
        time.sleep(0.01)  # Write command delay

        # Send content line by line
        for line in content.split("\n"):
            if line:  # Skip empty lines
                self.cli.send_raw(f"{line}\r\n".encode())
                time.sleep(0.01)  # Line delay

        # Send Ctrl+C to finish
        self.cli.send_raw(b"\x03")
        time.sleep(0.05)  # Write completion delay

        # Read response
        response = self.cli.read_available(timeout=1)
        decoded = response.decode("utf-8", errors="replace")

        if "Error" in decoded:
            raise WriteError(f"Failed to write {file_path}: {decoded}")

        self.logger.info(f"Successfully wrote {file_path}")
        return True

    def stat(self, path: str) -> Optional[Dict[str, Union[str, int]]]:
        """Get file or directory statistics."""
        response = self.cli.send_command(f"storage stat {path}")

        if "File, size:" in response:
            # Parse file stats
            size_str = response.split("size:")[1].split()[0]
            size = int(size_str.rstrip("b"))
            return {"type": "file", "size": size, "path": path}
        elif "Dir" in response:
            return {"type": "directory", "path": path}

        return None

    def exists(self, path: str) -> bool:
        """Check if file or directory exists."""
        return self.stat(path) is not None

    def remove(self, path: str) -> bool:
        """Remove file or directory."""
        response = self.cli.send_command(f"storage remove {path}")

        if "Error" in response:
            raise FlipperFilesystemError(f"Failed to remove {path}: {response}")

        return True

    def mkdir(self, path: str) -> bool:
        """Create directory."""
        response = self.cli.send_command(f"storage mkdir {path}")

        if "Error" in response:
            raise FlipperFilesystemError(
                f"Failed to create directory {path}: {response}"
            )

        return True

    def read_binary(self, file_path: str, chunk_size: int = 1024) -> bytes:
        """Read binary file using chunk operations."""
        content = b""
        offset = 0

        while True:
            response = self.cli.send_command(
                f"storage read_chunks {file_path} {chunk_size}", timeout=5
            )

            # Parse response for binary data
            if "Size:" in response:
                # Extract hex data and convert to bytes
                hex_lines = []
                for line in response.split("\n"):
                    # Look for hex data patterns
                    if re.match(r"^[0-9A-Fa-f\s]+$", line.strip()):
                        hex_lines.append(line.strip())

                if hex_lines:
                    hex_data = "".join(hex_lines).replace(" ", "")
                    chunk = bytes.fromhex(hex_data)
                    content += chunk

                    if len(chunk) < chunk_size:
                        break  # End of file
                    offset += chunk_size
                else:
                    break
            else:
                break

        return content

    def write_binary(self, file_path: str, data: bytes, chunk_size: int = 1024) -> bool:
        """Write binary file using chunk operations."""
        offset = 0
        total_size = len(data)

        while offset < total_size:
            chunk = data[offset : offset + chunk_size]
            hex_data = chunk.hex()

            # Send write_chunk command
            self.cli.send_raw(
                f"storage write_chunk {file_path} {len(chunk)}\r".encode()
            )
            time.sleep(0.2)

            # Send hex data
            for i in range(0, len(hex_data), 64):  # Send in lines of 64 chars
                line = hex_data[i : i + 64]
                self.cli.send_raw(f"{line}\r".encode())
                time.sleep(0.05)

            # End chunk
            self.cli.send_raw(b"\x03")
            time.sleep(0.3)

            response = self.cli.read_available()
            if b"Error" in response:
                raise WriteError(f"Failed to write chunk at offset {offset}")

            offset += chunk_size

        return True

    def copy(self, source: str, destination: str) -> bool:
        """Copy file to new location."""
        response = self.cli.send_command(f"storage copy {source} {destination}")

        if "Error" in response:
            raise FlipperFilesystemError(f"Failed to copy {source} to {destination}")

        return True

    def rename(self, old_path: str, new_path: str) -> bool:
        """Rename or move file."""
        response = self.cli.send_command(f"storage rename {old_path} {new_path}")

        if "Error" in response:
            raise FlipperFilesystemError(f"Failed to rename {old_path} to {new_path}")

        return True

    def md5(self, file_path: str) -> str:
        """Calculate MD5 hash of file."""
        response = self.cli.send_command(f"storage md5 {file_path}")

        # Extract MD5 hash from response
        for line in response.split("\n"):
            if re.match(r"^[0-9a-f]{32}$", line.strip()):
                return line.strip()

        raise FlipperFilesystemError(f"Failed to get MD5 for {file_path}")

    def tree(self, path: str = "/any") -> str:
        """Get recursive directory listing."""
        response = self.cli.send_command(f"storage tree {path}", timeout=10)

        # Clean up response
        lines = []
        for line in response.split("\n"):
            if not line.startswith(">") and line.strip():
                lines.append(line)

        return "\n".join(lines)

    def close(self):
        """Close connection."""
        self.cli.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
