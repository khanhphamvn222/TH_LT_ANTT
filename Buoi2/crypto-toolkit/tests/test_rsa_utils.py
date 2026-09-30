from securecrypto import rsa_utils


def test_rsa_keypair_generation():
    private_key, public_key = rsa_utils.generate_rsa_keypair()
    assert private_key is not None
    assert public_key is not None


def test_sign_and_verify():
    private_key, public_key = rsa_utils.generate_rsa_keypair()
    data = b"Test data for signing"
    signature = rsa_utils.sign_data_rsa(data, private_key)

    assert rsa_utils.verify_signature_rsa(data, signature, public_key) is True
    assert rsa_utils.verify_signature_rsa(b"Tampered data", signature, public_key) is False
