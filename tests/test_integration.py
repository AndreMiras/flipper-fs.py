"""Integration tests for flipperfs module."""

import pytest
import tempfile
from flipperfs import FlipperStorage
from flipperfs.utils import create_sub_content


@pytest.fixture
def temp_test_file():
    """Create temporary test file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sub', delete=False) as f:
        f.write(create_sub_content('00000012F6CC053C'))
        return f.name


def test_integration_with_controller():
    """Test integration with FlipperController."""
    from flipperfs import FlipperStorage

    # This is a placeholder for integration test structure
    # Actual integration tests would require a real device
    assert FlipperStorage is not None