import socket
import threading
from rsa_utils import *

HOST = "127.0.0.1"
PORT = 5555
BUFFER_SIZE = 4096

clients = {}


def broadcast(sender, message):
    for conn, public_key in clients.items():
        if conn != sender:
            encrypted = encrypt_message(public_key, message)
            conn.send(encrypted)


def handle_client(conn):
    # Create RSA keys
    private_key, public_key = generate_keys()

    # Send server public key
    conn.send(serialize_public_key(public_key))

    # Receive client public key
    client_public_key = load_public_key(conn.recv(BUFFER_SIZE))

    # Save client
    clients[conn] = client_public_key

    while True:
        try:
            # Receive encrypted message
            encrypted_msg = conn.recv(BUFFER_SIZE)

            if not encrypted_msg:
                break

            # Decrypt message
            message = decrypt_message(private_key, encrypted_msg)

            print("Message:", message)

            # Send to everyone else
            broadcast(conn, message)

        except:
            break

    conn.close()
    del clients[conn]


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server started...")

    while True:
        conn, addr = server.accept()
        print("Connected:", addr)

        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()


start_server()