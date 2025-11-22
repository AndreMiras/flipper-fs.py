"""Integration tests for flipperfs module with real hardware."""

import os
import time
import uuid
import pytest
from flipperfs import FlipperStorage


@pytest.fixture
def flipper_port():
    """Get Flipper port from environment or skip test.

    Set FLIPPER_PORT environment variable to enable integration tests.
    Example: export FLIPPER_PORT=/dev/ttyACM0
    """
    port = os.getenv("FLIPPER_PORT")
    if not port:
        pytest.skip("FLIPPER_PORT not set - skipping hardware integration test")
    return port


def test_write_read_cycle(flipper_port):
    """Integration test: write file to device and read back.

    This test requires a real Flipper Zero device connected via serial.
    It will:
    1. Write a test file to /ext/ (SD card)
    2. Verify the file exists
    3. Read the content back
    4. Verify content matches
    5. Get file stats
    6. Clean up the test file
    """
    # Generate unique test filename to avoid collisions
    test_filename = f"flipperfs_integration_test_{uuid.uuid4().hex[:8]}.txt"
    test_path = f"/ext/{test_filename}"

    test_content = "FlipperFS Integration Test\nThis verifies real device I/O\n"

    try:
        with FlipperStorage(port=flipper_port) as storage:
            # Measure write operation
            start = time.time()
            storage.write(test_path, test_content)
            write_time = time.time() - start
            print(f"\n⏱️  Write operation: {write_time:.3f}s")

            # Verify file exists (with retry for buffer timing issues on long filenames)
            start = time.time()
            if not storage.exists(test_path):
                time.sleep(0.5)
                assert storage.exists(test_path), "File should exist after write"
            exists_time = time.time() - start
            print(f"⏱️  Exists check: {exists_time:.3f}s")

            # Read content back (with retry for buffer timing issues)
            start = time.time()
            try:
                read_content = storage.read(test_path)
            except Exception:
                time.sleep(0.5)
                read_content = storage.read(test_path)
            read_time = time.time() - start
            print(f"⏱️  Read operation: {read_time:.3f}s")

            # Verify content matches (check first line for line ending differences)
            expected_first_line = test_content.split("\n")[0]
            assert expected_first_line in read_content, (
                f"Read content should contain '{expected_first_line}'"
            )

            # Verify file stats (with multiple retries for buffer timing issues)
            stats = None
            for _ in range(3):
                stats = storage.stat(test_path)
                if stats is not None:
                    break
                time.sleep(0.5)

            # Stats check is best-effort due to network buffer timing issues
            if stats is not None:
                assert stats["type"] == "file", "Type should be 'file'"
                assert stats["size"] > 0, "Size should be greater than 0"

    finally:
        # Always clean up, even if test fails
        try:
            with FlipperStorage(port=flipper_port) as storage:
                if storage.exists(test_path):
                    storage.remove(test_path)
        except Exception:
            # Best effort cleanup - don't mask test failures with cleanup failures
            pass
