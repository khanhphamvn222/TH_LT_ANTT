import os
import sys

from cryptography import x509

from ca_utils import (
    create_intermediate_ca,
    create_root_ca,
    issue_certificate,
    load_cert,
    verify_certificate_chain,
)
from revoke_utils import check_revocation_status, revoke_certificate


try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def setup_ca():
    print("Tao Root CA...")
    root_key, root_cert = create_root_ca()
    print("Root CA da tao: certs/root_ca_cert.pem, certs/root_ca_key.pem")

    print("Tao Intermediate CA...")
    inter_key, inter_cert = create_intermediate_ca(root_key, root_cert)
    print("Intermediate CA da tao: certs/intermediate_cert.pem, certs/intermediate_key.pem")
    return root_key, root_cert, inter_key, inter_cert


def issue_cert_demo(inter_key, inter_cert):
    subject_info = {
        "common_name": "Pham Duy Khanh 2387700029",
        "org": "HUTECH Security",
        "country": "VN",
    }
    print("Phat hanh chung chi nguoi dung cuoi...")
    issue_certificate(inter_key, inter_cert, subject_info)
    cert_path = os.path.join("certs", "Pham_Duy_Khanh_2387700029_cert.pem")
    key_path = os.path.join("certs", "Pham_Duy_Khanh_2387700029_key.pem")
    print(f"Da phat hanh: {cert_path}, {key_path}")
    return cert_path


def verify_chain_demo(user_cert_path):
    print("Kiem tra chuoi chung chi...")
    user_cert = load_cert(user_cert_path)
    chain_certs = [
        load_cert(os.path.join("certs", "intermediate_cert.pem")),
        load_cert(os.path.join("certs", "root_ca_cert.pem")),
    ]
    valid = verify_certificate_chain(user_cert, chain_certs)
    print(f"Chuoi hop le: {valid}")
    return valid


def revoke_demo():
    print("Thu hoi chung chi Pham Duy Khanh...")
    revoke_certificate(
        os.path.join("certs", "Pham_Duy_Khanh_2387700029_cert.pem"),
        os.path.join("certs", "intermediate_cert.pem"),
        os.path.join("certs", "intermediate_key.pem"),
        reason=x509.ReasonFlags.key_compromise,
    )
    print("Da thu hoi va cap nhat certs/ca_crl.pem")


def ocsp_check_demo():
    print("Kiem tra trang thai OCSP cua Pham_Duy_Khanh_2387700029_cert.pem...")
    revoked = check_revocation_status(os.path.join("certs", "Pham_Duy_Khanh_2387700029_cert.pem"))
    print(f"Trang thai: {'Revoked' if revoked else 'Valid'}")
    return revoked


def run_all():
    _, _, inter_key, inter_cert = setup_ca()
    user_cert = issue_cert_demo(inter_key, inter_cert)
    verify_chain_demo(user_cert)
    revoke_demo()
    ocsp_check_demo()


if __name__ == "__main__":
    run_all()
