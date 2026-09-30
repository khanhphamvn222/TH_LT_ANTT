from ca_utils import (
    check_ocsp_status,
    create_intermediate_ca,
    create_root_ca,
    issue_certificate,
    revoke_certificate,
    verify_certificate_chain,
)


def main():
    root_ca = create_root_ca()
    intermediate_ca = create_intermediate_ca(root_ca)
    _, server_cert = issue_certificate(
        intermediate_ca,
        {
            "country": "VN",
            "organization": "HUTECH",
            "common_name": "student.local",
        },
    )

    chain_ok = verify_certificate_chain(server_cert, [intermediate_ca[1], root_ca[1]])
    print(f"Certificate chain valid: {chain_ok}")
    print(f"OCSP before revoke: {check_ocsp_status(server_cert.serial_number)}")

    revoke_certificate(server_cert.serial_number, "key_compromise")
    print(f"OCSP after revoke: {check_ocsp_status(server_cert.serial_number)}")


if __name__ == "__main__":
    main()
