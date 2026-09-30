from ca_utils import (
    check_ocsp_status,
    create_intermediate_ca,
    create_root_ca,
    issue_certificate,
    revoke_certificate,
    verify_certificate_chain,
)


def test_create_ca_chain_and_issue_certificate():
    root_ca = create_root_ca()
    intermediate_ca = create_intermediate_ca(root_ca)
    _, cert = issue_certificate(
        intermediate_ca,
        {"country": "VN", "organization": "HUTECH", "common_name": "student.local"},
    )

    assert verify_certificate_chain(cert, [intermediate_ca[1], root_ca[1]]) is True


def test_revoke_certificate_and_ocsp_status():
    root_ca = create_root_ca()
    intermediate_ca = create_intermediate_ca(root_ca)
    _, cert = issue_certificate(intermediate_ca, {"common_name": "revoked.local"})

    assert check_ocsp_status(cert.serial_number) == "good"
    revoke_certificate(cert.serial_number, "key_compromise")
    assert check_ocsp_status(cert.serial_number) == "revoked"
    assert verify_certificate_chain(cert, [intermediate_ca[1], root_ca[1]]) is False
