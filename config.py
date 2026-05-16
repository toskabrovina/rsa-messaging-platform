"""
Configuration Module
====================
Centralized configuration constants used by both the server and client.

Optional pattern (not enabled here): these values can be sourced from
environment variables in future for easier deployment portability.
"""

from typing import Dict, Tuple

# Server host address (localhost for local development)
HOST = "127.0.0.1"

# Port number for the server to listen on
PORT = 5555

# Maximum buffer size for receiving data over the network (in bytes).
# RSA 2048-bit encryption produces 256-byte ciphertexts, so 4096 bytes
# provides ample room for encrypted messages and key exchange data.
BUFFER_SIZE = 4096


def get_server_address() -> Tuple[str, int]:
	"""Return the configured server address tuple for socket connect/bind."""
	return HOST, PORT


def validate_config() -> None:
	"""Validate runtime network configuration and raise ValueError if invalid."""
	if not isinstance(HOST, str) or not HOST.strip():
		raise ValueError("HOST must be a non-empty string.")

	if not isinstance(PORT, int) or not (1 <= PORT <= 65535):
		raise ValueError("PORT must be an integer between 1 and 65535.")

	# 256 bytes is the minimum ciphertext size for RSA-2048 operations.
	if not isinstance(BUFFER_SIZE, int) or BUFFER_SIZE < 256:
		raise ValueError("BUFFER_SIZE must be an integer >= 256.")


def get_config_info() -> Dict[str, int | str]:
	"""Return a compact summary of current configuration values."""
	return {
		"host": HOST,
		"port": PORT,
		"buffer_size": BUFFER_SIZE,
	}
