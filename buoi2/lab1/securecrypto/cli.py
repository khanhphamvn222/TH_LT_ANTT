import argparse

from securecrypto import aes_utils


def main(argv=None):
    parser = argparse.ArgumentParser(description="SecureCrypto CLI")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--encrypt", help="Encrypt file")
    action.add_argument("--decrypt", help="Decrypt file")
    parser.add_argument(
        "--password",
        required=True,
        help="Password for AES encryption or base64 key for decryption",
    )
    args = parser.parse_args(argv)

    if args.encrypt:
        key = aes_utils.encrypt_file_aes(args.encrypt, args.password)
        print(key)
        return key

    output_path = aes_utils.decrypt_file_aes(args.decrypt, args.password)
    print(f"Decrypted. Output: {output_path}")
    return output_path


if __name__ == "__main__":
    main()
