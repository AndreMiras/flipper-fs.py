"""Test suite for flipperfs.utils module."""

import pytest
from flipperfs.utils import (
    normalize_path,
    parse_size,
    format_sub_key,
    create_sub_content
)


class TestUtils:
    """Test utility functions."""

    def test_normalize_path(self):
        assert normalize_path('test') == '/test'
        assert normalize_path('/test/') == '/test'
        assert normalize_path('//test//file') == '/test/file'
        assert normalize_path('/') == '/'

    def test_parse_size(self):
        assert parse_size('158b') == 158
        assert parse_size('2KiB') == 2048
        assert parse_size('1MiB') == 1048576
        assert parse_size('1024') == 1024

    def test_format_sub_key(self):
        assert format_sub_key('00000012F6CC053C') == '00 00 00 12 F6 CC 05 3C'
        assert format_sub_key('00 00 00 12') == '00 00 00 12'

    def test_create_sub_content(self):
        content = create_sub_content('00000012F6CC053C')
        assert 'Filetype: Flipper SubGhz Key File' in content
        assert 'Key: 00 00 00 12 F6 CC 05 3C' in content
        assert 'Frequency: 433920000' in content