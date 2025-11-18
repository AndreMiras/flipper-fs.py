# FlipperFS

**Reliable Flipper Zero filesystem operations via serial CLI**

FlipperFS is a Python library that provides direct, reliable access to the Flipper Zero filesystem through serial communication at 230400 baud. Unlike other libraries with buggy storage operations, FlipperFS uses the proven serial CLI interface for rock-solid file operations.

## Features

- 🔌 **Direct Serial Communication** - No middleware, talks directly to Flipper CLI at 230400 baud
- 📁 **Complete Filesystem Operations** - read, write, list, stat, mkdir, remove, copy, rename
- 🔢 **Binary File Support** - Handle both text and binary files with chunk operations
- 📡 **Sub-GHz Utilities** - Optional specialized operations for Sub-GHz signal files
- 🛡️ **Robust Error Handling** - Custom exceptions with meaningful error messages
- 🐍 **Pythonic API** - Context managers, type hints, clean interfaces
- ✅ **Production Ready** - Comprehensive test coverage and proven in production

## Installation

```bash
pip install flipperfs
```

### Development Installation

```bash
git clone https://github.com/AndreMiras/flipper-fs.py.git
cd flipper-fs
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from flipperfs import FlipperStorage

# Connect to Flipper Zero
with FlipperStorage(port='/dev/ttyACM0') as storage:
    # List files
    files = storage.list('/any/subghz')
    print(f"Found {len(files)} items")

    # Read a file
    content = storage.read('/any/subghz/signal.sub')
    print(content)

    # Write a file
    storage.write('/any/test.txt', 'Hello from FlipperFS!')

    # Check if path exists
    if storage.exists('/any/subghz'):
        print("Sub-GHz directory exists")

    # Get file info
    info = storage.stat('/any/test.txt')
    print(f"File size: {info['size']} bytes")

    # Clean up
    storage.remove('/any/test.txt')
```

### Sub-GHz Operations

```python
from flipperfs.extras import SubGhzStorage

with SubGhzStorage(port='/dev/ttyACM0') as subghz:
    # List all signal files
    signals = subghz.list_signals()
    print(f"Found {len(signals)} signal files")

    # Read and parse signal file
    signal_data = subghz.read_signal('my_signal.sub')
    print(f"Frequency: {signal_data['Frequency']}")
    print(f"Protocol: {signal_data['Protocol']}")

    # Create a new signal file
    subghz.write_signal(
        signal_name='test_signal',
        hex_key='00000012F6CC053C',
        frequency=433920000,
        protocol='Dooya',
        bit_length=40
    )

    # Create temporary signal for transmission
    temp_path = subghz.create_temp_signal(
        hex_key='00000012F6CC053C',
        protocol='Dooya'
    )
    print(f"Temp signal created at: {temp_path}")

    # Clean up
    subghz.remove(temp_path)
```

## API Reference

### FlipperStorage

Main class for filesystem operations.

#### Connection

```python
storage = FlipperStorage(port='/dev/ttyACM0', baud_rate=230400)
```

Parameters:
- `port` (str): Serial port path (default: `/dev/ttyACM0`)
- `baud_rate` (int): Serial baud rate (default: `230400`)

#### Methods

**`info(path='/any') -> Dict[str, str]`**
Get filesystem information (size, free space, etc.)

**`list(path='/any') -> List[Dict[str, Union[str, int]]]`**
List files and directories. Returns list of dicts with keys: `type`, `name`, `size`, `path`

**`read(file_path) -> str`**
Read text file content

**`write(file_path, content) -> bool`**
Write text content to file

**`read_binary(file_path, chunk_size=1024) -> bytes`**
Read binary file using chunk operations

**`write_binary(file_path, data, chunk_size=1024) -> bool`**
Write binary data to file using chunk operations

**`stat(path) -> Optional[Dict[str, Union[str, int]]]`**
Get file or directory statistics

**`exists(path) -> bool`**
Check if file or directory exists

**`remove(path) -> bool`**
Delete file or directory

**`mkdir(path) -> bool`**
Create directory

**`copy(source, destination) -> bool`**
Copy file to new location

**`rename(old_path, new_path) -> bool`**
Rename or move file

**`md5(file_path) -> str`**
Calculate MD5 hash of file

**`tree(path='/any') -> str`**
Get recursive directory listing as formatted string

**`close()`**
Close serial connection

### SubGhzStorage

Extended storage operations for Sub-GHz signal files (inherits from FlipperStorage).

#### Methods

**`list_signals(directory='/any/subghz') -> List[str]`**
List all .sub signal files in directory

**`read_signal(signal_name) -> Dict[str, str]`**
Read and parse .sub file content into dictionary

**`write_signal(signal_name, hex_key, frequency=433920000, protocol='Dooya', preset='FuriHalSubGhzPresetOok650Async', bit_length=40) -> bool`**
Create a new .sub signal file with specified parameters

**`create_temp_signal(hex_key, **kwargs) -> str`**
Create temporary signal file and return path

### Exceptions

All exceptions inherit from `FlipperFilesystemError`:

- `ConnectionError` - Failed to connect or communicate with Flipper
- `FileNotFoundError` - File or directory not found on Flipper
- `WriteError` - Failed to write file to Flipper
- `ReadError` - Failed to read file from Flipper

## Environment Variables

You can set default values via environment variables:

```bash
export FLIPPER_PORT=/dev/ttyACM1
export FLIPPER_BAUD=230400
```

Then in your code:

```python
import os
from flipperfs import FlipperStorage

port = os.getenv('FLIPPER_PORT', '/dev/ttyACM0')
storage = FlipperStorage(port=port)
```

## Serial Port Detection

On Linux, Flipper Zero typically appears as `/dev/ttyACM0` or `/dev/ttyACM1`.

To find your Flipper's port:

```bash
# List serial ports
ls /dev/tty* | grep ACM

# Or use dmesg
dmesg | grep tty
```

On macOS:
```bash
ls /dev/cu.usbmodem*
```

On Windows:
```
# Check Device Manager for COM ports
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=flipperfs --cov-report=html
```

### Code Formatting

```bash
# Format code
black flipperfs tests examples

# Check style
flake8 flipperfs tests examples

# Type checking
mypy flipperfs
```

## Examples

See the `examples/` directory for complete examples:

- `basic_operations.py` - Basic filesystem operations
- `binary_files.py` - Binary file handling
- `subghz_signals.py` - Sub-GHz signal management

## Why FlipperFS?

Existing libraries like PyFlipper have known bugs in their storage operations, particularly with file writes. FlipperFS was built from the ground up using direct serial CLI communication, which has proven reliable in production.

### Advantages

- ✅ **Proven reliability** - Battle-tested in production environments
- ✅ **Direct serial** - No wrapper layers to cause issues
- ✅ **Complete API** - All filesystem operations supported
- ✅ **Well tested** - Comprehensive test suite
- ✅ **Clean code** - Well-structured, documented, maintainable

## Troubleshooting

### Permission Denied on Linux

Add your user to the `dialout` group:

```bash
sudo usermod -a -G dialout $USER
# Log out and back in for changes to take effect
```

Or run with sudo (not recommended):
```bash
sudo python your_script.py
```

### Connection Timeout

- Ensure Flipper is powered on
- Check the serial port is correct (`ls /dev/tty*`)
- Verify no other programs are using the serial port
- Try unplugging and replugging the USB cable

### Import Errors

Make sure pyserial is installed:
```bash
pip install pyserial
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run the test suite
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

Developed to provide reliable filesystem operations for Flipper Zero devices.

## Links

- **Repository**: https://github.com/AndreMiras/flipper-fs.py
- **Issues**: https://github.com/AndreMiras/flipper-fs.py/issues
- **PyPI**: https://pypi.org/project/flipperfs/
- **Flipper Zero**: https://flipperzero.one/
