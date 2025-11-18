"""Low-level serial CLI communication with Flipper Zero."""

import serial
import time
import logging
from typing import Optional
from .exceptions import ConnectionError


class SerialCLI:
    """Handles serial communication with Flipper Zero CLI."""

    DEFAULT_BAUD_RATE = 230400
    DEFAULT_TIMEOUT = 1
    COMMAND_TIMEOUT = 3
    PROMPT = b'>:'

    def __init__(self, port: str = '/dev/ttyACM0', baud_rate: int = None):
        """Initialize serial connection to Flipper."""
        self.port = port
        self.baud_rate = baud_rate or self.DEFAULT_BAUD_RATE
        self.serial = None
        self.logger = logging.getLogger(__name__)
        self.connect()

    def connect(self):
        """Establish serial connection."""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=self.DEFAULT_TIMEOUT,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            time.sleep(0.5)  # Stabilization delay
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
            self.logger.info(f"Connected to {self.port} at {self.baud_rate} baud")
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to connect to {self.port}: {e}")

    def send_command(self, command: str, timeout: float = None) -> str:
        """Send command and return response."""
        if not self.serial or not self.serial.is_open:
            raise ConnectionError("Serial connection not open")

        timeout = timeout or self.COMMAND_TIMEOUT
        self.logger.debug(f"Sending: {command}")

        # Send command
        self.serial.write(f"{command}\r".encode())
        self.serial.flush()

        # Read response until prompt
        response = b''
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.serial.in_waiting:
                chunk = self.serial.read(self.serial.in_waiting)
                response += chunk

                if self.PROMPT in response:
                    break
            time.sleep(0.05)

        decoded = response.decode('utf-8', errors='replace')
        self.logger.debug(f"Response: {decoded[:100]}...")
        return decoded

    def send_raw(self, data: bytes):
        """Send raw bytes without waiting for response."""
        if not self.serial or not self.serial.is_open:
            raise ConnectionError("Serial connection not open")
        self.serial.write(data)
        self.serial.flush()

    def read_available(self, timeout: float = 1) -> bytes:
        """Read all available data within timeout."""
        data = b''
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.serial.in_waiting:
                data += self.serial.read(self.serial.in_waiting)
            else:
                time.sleep(0.05)

        return data

    def close(self):
        """Close serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.logger.info("Serial connection closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
