"""
RSA Encrypted Chat Server
==========================

Nje server chat-i me shume kliente qe perdor enkriptimin me celes publik RSA per te siguruar qe te gjitha mesazhet e shkembyera ndermjet klienteve te jene konfidenciale.

Si funksionon:

1. Serveri gjeneron nje cift unik celesash RSA per secilin klient qe lidhet.
2. Pas lidhjes, serveri dhe klienti shkembejne celesat publike.
3. Te gjitha mesazhet nga klientet enkriptohen me celesin publik te serverit, dekriptohen nga serveri dhe me pas ri-enkriptohen me celesin publik te secilit klient marres perpara se te transmetohen.
4. celesat private nuk largohen kurre nga pajisja qe i ka gjeneruar.

"""

import socket
import threading
from rsa_utils import (
    generate_keys, serialize_public_key, load_public_key,
    encrypt_message, decrypt_message
)
from config import HOST, PORT, BUFFER_SIZE, validate_config

# Dictionary storing connected clients.
# Maps connection object -> {"username": str, "public_key": RSA public key}
clients = {}

# Lock for thread-safe access to the shared clients dictionary
clients_lock = threading.Lock()


def get_client_count():
    """Return current number of connected clients."""
    with clients_lock:
        return len(clients)


def get_connected_usernames():
    """Return a snapshot list of connected usernames."""
    with clients_lock:
        return [info["username"] for info in clients.values()]


def broadcast(sender_conn, message):
    """
    Transmeton nje mesazh te te gjithe klientet e lidhur, pervec derguesit.

    Mesazhi enkriptohet individualisht me celesin publik te secilit marres perpara se te dergohet, duke siguruar konfidencialitet nga nje skaj ne tjetrin (*end-to-end confidentiality*).

    **Argumentet:**

    * `sender_conn`: Objekti i lidhjes se derguesit (i perjashtuar nga transmetimi).
    * `message (str)`: Mesazhi ne tekst te thjeshte qe do te enkriptohet dhe transmetohet.

    """
    # Snapshot recipients under lock, then perform network I/O outside lock.
    with clients_lock:
        recipients = [
            (conn, info)
            for conn, info in clients.items()
            if conn != sender_conn
        ]

    stale_connections = []
    for conn, client_info in recipients:
        try:
            # Encrypt the message with this specific client's public key
            encrypted = encrypt_message(client_info["public_key"], message)
            conn.send(encrypted)
        except (ConnectionResetError, BrokenPipeError, OSError) as e:
            print(f"[ERROR] Failed to send to {client_info['username']}: {e}")
            stale_connections.append(conn)

    if stale_connections:
        with clients_lock:
            for conn in stale_connections:
                if conn in clients:
                    del clients[conn]
                try:
                    conn.close()
                except OSError:
                    pass


def handle_client(conn, addr):
    """
        Trajton ciklin e plote te jetes se nje lidhjeje te vetme me klientin:

        1. Gjeneron ciftin e celesave RSA per kete sesion.
        2. Shkemben celesat publike me klientin.
        3. Merr emrin e perdoruesit te enkriptuar te klientit.
        4. Hyn ne ciklin e mesazheve: merr, dekripton dhe transmeton mesazhet.
        5. Pastron burimet pas shkeputjes.

        **Argumentet:**

        * `conn`: Objekti i lidhjes socket per kete klient.
        * `addr`: Tupla `(host, port)` e adreses se klientit.

    """
    print(f"New client connected from {addr}. Exchanging public keys...")

    # Step 1: Generate a unique RSA key pair for communicating with this client
    private_key, public_key = generate_keys()

    try:
        # Step 2: Send the server's public key to the client
        conn.send(serialize_public_key(public_key))

        # Step 3: Receive the client's public key
        client_public_key_data = conn.recv(BUFFER_SIZE)
        if not client_public_key_data:
            print(f"[ERROR] {addr}: No public key received. Closing connection.")
            conn.close()
            return

        client_public_key = load_public_key(client_public_key_data)
        print(f"Public key exchange complete with {addr}.")

        # Step 4: Receive the client's username (encrypted with server's public key)
        encrypted_username = conn.recv(BUFFER_SIZE)
        if not encrypted_username:
            print(f"[ERROR] {addr}: No username received. Closing connection.")
            conn.close()
            return

        username = decrypt_message(private_key, encrypted_username)

        # Step 5: Register the client in the connected clients dictionary
        with clients_lock:
            clients[conn] = {
                "username": username,
                "public_key": client_public_key
            }
            active_clients = len(clients)

        print(f"[CONNECTED] {username} has joined the chat.")
        print(f"Ready to receive encrypted messages from {username}.")
        print(f"[INFO] Active clients: {active_clients}")

        # Notify other clients that a new user has joined
        broadcast(conn, f">> {username} has joined the chat.")

        # Step 6: Main message loop — receive, decrypt, and broadcast
        while True:
            encrypted_msg = conn.recv(BUFFER_SIZE)
            if not encrypted_msg:
                break

            message = decrypt_message(private_key, encrypted_msg)
            full_msg = f"{username}: {message}"

            print(f"[MESSAGE] {full_msg}")
            broadcast(conn, full_msg)

    except ConnectionResetError:
        print(f"[ERROR] {addr}: Client disconnected unexpectedly.")
    except ValueError as e:
        print(f"[ERROR] {addr}: Decryption or key exchange failure — {e}")
    except OSError as e:
        print(f"[ERROR] {addr}: Network error — {e}")
    except Exception as e:
        print(f"[ERROR] {addr}: Unexpected error — {e}")

    finally:
        with clients_lock:
            if conn in clients:
                username = clients[conn]["username"]
                del clients[conn]
                print(f"[DISCONNECTED] {username} has left the chat.")
                print(f"[INFO] Active clients: {len(clients)}")
        if 'username' in dir():
            broadcast(conn, f">> {username} has left the chat.")

        conn.close()


def start_server():
    """
    Inicializon dhe nis serverin TCP.
    degjon per lidhjet hyrese te klienteve dhe krijon nje *thread* te ri 
    per secilin klient per te menaxhuar komunikimin paralel (*concurrent communication*).

    """
    validate_config()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started and listening for connections on {HOST}:{PORT}...")
    print("[INFO] RSA-2048 OAEP supports short plaintext messages only (roughly under 190 bytes).")
    print("Waiting for clients to connect...\n")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
