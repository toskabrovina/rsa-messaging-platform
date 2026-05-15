"""
Configuration Module
====================
Centralized configuration constants used by both the server and client.
"""

# Server host address (localhost for local development)
HOST = "127.0.0.1"

# Port number for the server to listen on
PORT = 5555

# Maximum buffer size for receiving data over the network (in bytes).
# RSA 2048-bit encryption produces 256-byte ciphertexts, so 4096 bytes
# provides ample room for encrypted messages and key exchange data.
BUFFER_SIZE = 4096
