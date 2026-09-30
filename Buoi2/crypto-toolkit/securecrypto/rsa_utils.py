from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def generate_rsa_keypair(key_size: int = 2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()
    return private_key, public_key


def sign_data_rsa(data: bytes, private_key) -> bytes:
    return private_key.sign(data, padding.PKCS1v15(), hashes.SHA256())


def verify_signature_rsa(data: bytes, signature: bytes, public_key) -> bool:
    try:
        public_key.verify(signature, data, padding.PKCS1v15(), hashes.SHA256())
        return True
    except InvalidSignature:
        return False


def private_key_to_pem(private_key) -> bytes:
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def public_key_to_pem(public_key) -> bytes:
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
