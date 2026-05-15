import socket
import threading
import sys
from rsa_utils import (
    generate_keys, serialize_public_key, load_public_key,
    encrypt_message, decrypt_message, get_public_key_info
)


from config import HOST, PORT, BUFFER_SIZE


def display_help():
    print("\n" + "=" * 50)
    print("  Available Commands:")
    print("=" * 50)
    print("  /help   — Show this help message")
    print("  /keys   — View public key details")
    print("  /exit   — Disconnect and exit the chat")
    print("=" * 50)
    print("  Type any other text to send an encrypted message.")
    print("=" * 50 + "\n")

def display_keys(own_public_key, server_public_key):
    print("\n" + "=" * 50)
    print("  Your Public Key:")
    print("=" * 50)
    print(get_public_key_info(own_public_key))
    print("=" * 50)
    print("  Server's Public Key:")
    print("=" * 50)
    print(get_public_key_info(server_public_key))
    print("=" * 50 + "\n")
