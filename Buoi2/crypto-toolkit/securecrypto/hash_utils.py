from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ph = PasswordHasher()


def hash_password_secure(password: str) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")
    return ph.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return ph.verify(password_hash, password)
    except VerifyMismatchError:
        return False
