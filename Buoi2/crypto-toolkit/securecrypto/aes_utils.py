import base64
import os
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
PBKDF2_ITERATIONS = 100_000


def derive_key_from_password(password: str, salt: bytes) -> bytes:
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")
    if len(salt) != SALT_SIZE:
        raise ValueError(f"Salt must be {SALT_SIZE} bytes")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=default_backend(),
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_file_aes(filepath, password: str) -> str:
    source_path = Path(filepath)
    if not source_path.is_file():
        raise FileNotFoundError(f"File not found: {source_path}")

    salt = os.urandom(SALT_SIZE)
    key = derive_key_from_password(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    data = source_path.read_bytes()
    ciphertext = aesgcm.encrypt(nonce, data, None)

    encrypted_path = source_path.with_name(source_path.name + ".enc")
    encrypted_path.write_bytes(salt + nonce + ciphertext)
    return base64.b64encode(key).decode("utf-8")


def decrypt_file_aes(encrypted_file, key_base64: str) -> str:
    encrypted_path = Path(encrypted_file)
    if not encrypted_path.is_file():
        raise FileNotFoundError(f"File not found: {encrypted_path}")

    raw = encrypted_path.read_bytes()
    if len(raw) <= SALT_SIZE + NONCE_SIZE:
        raise ValueError("Encrypted file is invalid or incomplete")

    nonce = raw[SALT_SIZE : SALT_SIZE + NONCE_SIZE]
    ciphertext = raw[SALT_SIZE + NONCE_SIZE :]
    key = base64.b64decode(key_base64)
    if len(key) != KEY_SIZE:
        raise ValueError("AES key must be 32 bytes after base64 decoding")

    plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
    output_path = _decrypted_output_path(encrypted_path)
    output_path.write_bytes(plaintext)
    return str(output_path)


def _decrypted_output_path(encrypted_path: Path) -> Path:
    if encrypted_path.name.endswith(".enc"):
        return encrypted_path.with_name(encrypted_path.name[:-4] + ".dec")
    return encrypted_path.with_name(encrypted_path.name + ".dec")
