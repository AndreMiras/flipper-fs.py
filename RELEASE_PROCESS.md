# FlipperFS Release Process

Complete guide for releasing new versions of FlipperFS to PyPI.

## Overview

- **Version Management**: Automated via setuptools-scm from git tags
- **Distribution**: Automated via GitHub Actions on tag push
- **Changelog**: Manual updates required before release
- **Versioning**: Follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## Pre-Release Checklist

Before creating a release, ensure all of the following are complete:

- [ ] All CI tests passing on main branch ([check workflows](https://github.com/AndreMiras/flipper-fs.py/actions))
- [ ] All planned features/fixes are merged to main
- [ ] No pending pull requests that should be included
- [ ] Version number decided following semver (e.g., `1.0.1`, `1.1.0`, `2.0.0`)
- [ ] CHANGELOG.md updated with new version section
- [ ] Documentation is up to date (README.md, docstrings, examples)
- [ ] Local testing completed successfully

## Release Steps

### 1. Update CHANGELOG.md

Add a new version section following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

### Removed
- Deprecated features removed

[X.Y.Z]: https://github.com/AndreMiras/flipper-fs.py/releases/tag/vX.Y.Z
```

Commit the changelog update:

```bash
git add CHANGELOG.md
git commit -m "Update CHANGELOG for v1.0.1 release"
git push origin main
```

### 2. Create and Push Git Tag

The version is derived from the git tag. Create an annotated tag:

```bash
# For patch release (bug fixes)
git tag -a v1.0.1 -m "Release 1.0.1"

# For minor release (new features, backward compatible)
git tag -a v1.1.0 -m "Release 1.1.0"

# For major release (breaking changes)
git tag -a v2.0.0 -m "Release 2.0.0"
```

Push the tag to trigger the release:

```bash
git push origin v1.0.1
```

**Important**: The tag must start with `v` followed by the version number (e.g., `v1.0.1`).

### 3. Monitor GitHub Actions

After pushing the tag, GitHub Actions will automatically:
1. Build the package (wheel and source distribution)
2. Validate the build with `twine check`
3. Publish to PyPI using the `PYPI_API_TOKEN` secret

Monitor the workflow progress:
- Go to: https://github.com/AndreMiras/flipper-fs.py/actions
- Click on the "Publish to PyPI" workflow
- Watch for successful completion (green checkmark)

The workflow typically completes within 2-3 minutes.

### 4. Verify PyPI Publication

Once the workflow completes, verify the release on PyPI:

**Check PyPI Page:**
- Visit: https://pypi.org/project/flipper-fs/
- Confirm the new version is listed
- Verify the release date and files

**Test Installation:**

```bash
# In a clean environment
python -m venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate

# Install the new version
pip install --upgrade flipper-fs

# Verify version
python -c "import flipperfs; print(flipperfs.__version__)"
```

The output should show the new version number (e.g., `1.0.1`).

## Post-Release Verification

After the release is published, perform these checks:

- [ ] Package appears on PyPI with correct version
- [ ] Installation works from PyPI (`pip install flipper-fs`)
- [ ] Version number is correct (`import flipperfs; flipperfs.__version__`)
- [ ] GitHub release created (optional: create release notes from tag)
- [ ] All platforms can install (check different OS if possible)
- [ ] Basic smoke test passes (import and basic operation)

## Version Management Details

FlipperFS uses **setuptools-scm** for automatic version management:

- **Release versions**: Derived from git tags (e.g., tag `v1.0.1` → version `1.0.1`)
- **Development versions**: Auto-generated with commit distance (e.g., `1.0.1.dev5` for 5 commits after v1.0.0)
- **No manual updates needed**: Version is never hardcoded in the codebase
- **Configuration**: See `pyproject.toml` lines 53-55

### How It Works:

1. setuptools-scm reads the git repository tags
2. Finds the most recent tag matching `v*` pattern
3. Strips the `v` prefix to get the version number
4. Adds `.devN` suffix for commits after the tag (development versions)
5. Embeds the version in the built package metadata

## Quick Reference

```bash
# Standard release workflow
git checkout main
git pull origin main

# Update CHANGELOG.md, then:
git add CHANGELOG.md
git commit -m "Update CHANGELOG for vX.Y.Z release"
git push origin main

# Create and push tag
git tag -a vX.Y.Z -m "Release X.Y.Z"
git push origin vX.Y.Z

# Monitor at: https://github.com/AndreMiras/flipper-fs.py/actions
# Verify at: https://pypi.org/project/flipper-fs/
```

## Additional Resources

- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [setuptools-scm Documentation](https://github.com/pypa/setuptools_scm/)
- [PyPI Help](https://pypi.org/help/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
