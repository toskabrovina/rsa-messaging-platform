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

def receive_messages(client_socket, private_key):
    while True:
        try:
            encrypted_msg = client_socket.recv(BUFFER_SIZE)
            if not encrypted_msg:
                print("\n[DISCONNECTED] Server closed the connection.")
                break

            message = decrypt_message(private_key, encrypted_msg)
            print(f"\n{message}")
            print("Enter message: ", end="", flush=True)

        except ConnectionResetError:
            print("\n[ERROR] Connection to server was lost.")
            break
        except ValueError as e:
            print(f"\n[ERROR] Failed to decrypt message: {e}")
        except OSError:
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"[ERROR] Could not connect to server at {HOST}:{PORT}.")
        sys.exit(1)

    print(f"Connected to server at {HOST}:{PORT}. Exchanging public keys...")

    private_key, public_key = generate_keys()

    try:
        server_public_key_data = client_socket.recv(BUFFER_SIZE)
        if not server_public_key_data:
            print("[ERROR] Failed to receive server's public key.")
            client_socket.close()
            sys.exit(1)

        server_public_key = load_public_key(server_public_key_data)

        client_socket.send(serialize_public_key(public_key))

        print("Public key exchange complete.")

        username = input("Enter your username: ")
        client_socket.send(encrypt_message(server_public_key, username))

        print(f"\nWelcome, {username}!")
        display_help()

        recv_thread = threading.Thread(
            target=receive_messages,
            args=(client_socket, private_key),
            daemon=True
        )
        recv_thread.start()

        while True:
            msg = input("Enter message: ")

            if msg.strip().lower() == "/exit":
                print("Disconnecting...")
                break
            elif msg.strip().lower() == "/help":
                display_help()
                continue
            elif msg.strip().lower() == "/keys":
                display_keys(public_key, server_public_key)
                continue
            elif msg.strip() == "":
                continue

            try:
                encrypted_msg = encrypt_message(server_public_key, msg)
                client_socket.send(encrypted_msg)
                print(f"[Sent encrypted - {len(encrypted_msg)} bytes]")
            except Exception as e:
                print(f"[ERROR] {e}")
                break

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    start_client()


