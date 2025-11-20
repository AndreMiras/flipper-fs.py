# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-20

### Added
- Network connection support via tcp://, socket://, rfc2217://, and loop:// URLs

### Changed
- Migrated from Black and Flake8 to Ruff for linting and formatting (10-100x faster)
- Modernized pyproject.toml with SPDX license identifier format
- Updated setuptools minimum version requirement to 61.0.0
- Modernized package discovery configuration using setuptools.packages.find

### Fixed
- License deprecation warnings in pyproject.toml configuration

## [1.0.1] - 2025-11-19

### Changed
- Migrated to setuptools-scm for automatic version management from git tags
- Version is now automatically derived from git tags (no more manual version updates)

### Added
- Documentation for the release process in CLAUDE.md
- Version management details in project documentation

## [1.0.0] - 2025-11-18

### Added
- Initial release of FlipperFS
- Core filesystem operations (read, write, list, stat, mkdir, remove)
- Binary file support via chunk operations
- Sub-GHz signal file utilities in extras module
- Serial CLI communication at 230400 baud
- Context manager support for connections
- Comprehensive error handling with custom exceptions
- Full test suite with mocked serial communication
- Complete documentation and examples
- GitHub Actions workflows for CI/CD

### Features
- Direct serial communication with Flipper Zero CLI
- All standard filesystem operations
- Binary file read/write with chunking
- MD5 hash calculation
- File copy and rename operations
- Recursive directory tree listing
- Sub-GHz signal file creation and parsing
- Temporary signal file generation
- Python 3.7+ compatibility
- Cross-platform support (Linux, macOS, Windows)

### Documentation
- Comprehensive README with quickstart and examples
- API reference documentation
- Example scripts for basic operations, binary files, and Sub-GHz signals
- Contributing guidelines
- MIT License

[1.1.0]: https://github.com/yourusername/flipper-fs/releases/tag/v1.1.0
[1.0.1]: https://github.com/yourusername/flipper-fs/releases/tag/v1.0.1
[1.0.0]: https://github.com/yourusername/flipper-fs/releases/tag/v1.0.0
