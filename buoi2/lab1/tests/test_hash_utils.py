from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from securecrypto import hash_utils


def test_hash_password_and_verify():
    password = "StrongPass123!"
    hashed = hash_utils.hash_password_secure(password)
    assert hashed is not None

    ph = PasswordHasher()
    try:
        ph.verify(hashed, password)
        verified = True
    except VerifyMismatchError:
        verified = False
    assert verified is True


def test_wrong_password_verification():
    password = "CorrectPass"
    wrong_password = "WrongPass"
    hashed = hash_utils.hash_password_secure(password)

    ph = PasswordHasher()
    try:
        ph.verify(hashed, wrong_password)
        verified = True
    except VerifyMismatchError:
        verified = False
    assert verified is False


def test_verify_password_helper():
    hashed = hash_utils.hash_password_secure("CorrectPass")
    assert hash_utils.verify_password(hashed, "CorrectPass") is True
    assert hash_utils.verify_password(hashed, "WrongPass") is False
