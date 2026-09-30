from securecrypto import hash_utils, rsa_utils


def main():
    password = "MatKhau@123"
    hashed = hash_utils.hash_password_secure(password)
    print("Argon2 hash:", hashed[:58] + "...")
    print("Verify correct:", hash_utils.verify_password(hashed, password))
    print("Verify wrong:", hash_utils.verify_password(hashed, "SaiMatKhau"))

    private_key, public_key = rsa_utils.generate_rsa_keypair()
    data = b"DuLieuQuanTrong"
    signature = rsa_utils.sign_data_rsa(data, private_key)
    print("RSA signature length:", len(signature))
    print("Verify original:", rsa_utils.verify_signature_rsa(data, signature, public_key))
    print("Detect tamper:", not rsa_utils.verify_signature_rsa(b"DuLieuBiSua", signature, public_key))


if __name__ == "__main__":
    main()
