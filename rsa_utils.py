from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def get_max_plaintext_size(key_size_bits=2048, hash_len_bytes=32):
    """Return OAEP maximum plaintext size in bytes for RSA.

    Formula: k - 2*hLen - 2, where k is key size in bytes.
    """
    key_size_bytes = key_size_bits // 8
    return key_size_bytes - (2 * hash_len_bytes) - 2


def generate_keys():
    """Generate an RSA-2048 key pair for a chat session."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()


def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def load_public_key(data):
    return serialization.load_pem_public_key(data)


def get_public_key_info(public_key):
    """Return a human-readable summary of an RSA public key."""
    numbers = public_key.public_numbers()
    return (
        f"Algorithm: RSA\n"
        f"Key Size: {public_key.key_size} bits\n"
        f"Public Exponent (e): {numbers.e}\n"
        f"Modulus (n) bit length: {numbers.n.bit_length()}"
    )


def encrypt_message(public_key, message):
    """Encrypt UTF-8 text with RSA OAEP-SHA256.

    Note: with 2048-bit RSA and OAEP-SHA256, practical plaintext size is
    limited to roughly 190 bytes per encryption operation.
    """
    return public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_message(private_key, ciphertext):
    """Decrypt ciphertext produced by encrypt_message and return text."""
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()