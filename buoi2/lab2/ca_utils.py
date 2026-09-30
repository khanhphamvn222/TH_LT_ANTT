import datetime
import os
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


BASE_DIR = Path(__file__).resolve().parent
CERTS_DIR = BASE_DIR / "certs"
CERTS_DIR.mkdir(exist_ok=True)

REVOKED_CERTS = {}


def generate_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def save_key(key, filename):
    path = CERTS_DIR / filename
    path.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    return str(path)


def save_cert(cert, filename):
    path = CERTS_DIR / filename
    path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    return str(path)


def load_key(filename):
    path = _resolve_cert_path(filename)
    return serialization.load_pem_private_key(path.read_bytes(), password=None)


def load_cert(filepath):
    path = _resolve_cert_path(filepath)
    return x509.load_pem_x509_certificate(path.read_bytes())


def create_root_ca():
    key = generate_key()
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Mini Root CA"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Mini Root CA Root"),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(_now())
        .not_valid_after(_now() + datetime.timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=1), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                key_encipherment=False,
                content_commitment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .sign(key, hashes.SHA256())
    )
    save_key(key, "root_ca_key.pem")
    save_cert(cert, "root_ca_cert.pem")
    return key, cert


def create_intermediate_ca(root_ca, root_cert=None):
    root_key, root_cert = _normalize_ca(root_ca, root_cert)
    key = generate_key()
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Mini Intermediate CA"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Mini Intermediate CA"),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(root_cert.subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(_now())
        .not_valid_after(_now() + datetime.timedelta(days=1825))
        .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                key_encipherment=False,
                content_commitment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .sign(root_key, hashes.SHA256())
    )
    save_key(key, "intermediate_key.pem")
    save_cert(cert, "intermediate_cert.pem")
    return key, cert


def issue_certificate(ca, ca_cert=None, subject_info=None):
    if isinstance(ca_cert, dict) and subject_info is None:
        subject_info = ca_cert
        ca_cert = None
    ca_key, ca_cert = _normalize_ca(ca, ca_cert)
    if subject_info is None:
        subject_info = {}
    key = generate_key()
    common_name = subject_info.get("common_name") or subject_info.get("cn") or "example.local"
    organization = subject_info.get("organization") or subject_info.get("org") or "End Entity"
    country = subject_info.get("country") or "VN"
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(_now())
        .not_valid_after(_now() + datetime.timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=False,
                crl_sign=False,
                key_encipherment=True,
                content_commitment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )
    safe_name = common_name.replace("*", "wildcard").replace(".", "_").replace(" ", "_")
    save_key(key, f"{safe_name}_key.pem")
    save_cert(cert, f"{safe_name}_cert.pem")
    return key, cert


def verify_certificate_chain(cert, ca_chain) -> bool:
    try:
        certificate = _normalize_cert(cert)
        chain = [_normalize_cert(item) for item in ca_chain]
        if not chain:
            return False
        _raise_if_expired(certificate)
        for ca_cert in chain:
            _raise_if_expired(ca_cert)
        current = certificate
        for issuer in chain:
            if current.issuer != issuer.subject:
                continue
            _verify_signed_by(current, issuer)
            current = issuer
        root = chain[-1]
        _verify_signed_by(root, root)
        return current.subject == root.subject and check_ocsp_status(certificate.serial_number) == "good"
    except Exception:
        return False


def revoke_certificate(cert_serial, reason="unspecified"):
    serial = _serial_to_int(cert_serial)
    REVOKED_CERTS[serial] = {
        "reason": reason,
        "revoked_at": _now(),
    }
    return REVOKED_CERTS[serial]


def check_ocsp_status(cert_serial):
    serial = _serial_to_int(cert_serial)
    return "revoked" if serial in REVOKED_CERTS else "good"


def _normalize_ca(ca, cert=None):
    if cert is not None:
        return ca, cert
    if isinstance(ca, tuple) and len(ca) == 2:
        return ca
    if isinstance(ca, dict):
        return ca["key"], ca["cert"]
    raise TypeError("CA must be a (key, cert) tuple or {'key': key, 'cert': cert} dict")


def _normalize_cert(cert):
    if isinstance(cert, x509.Certificate):
        return cert
    return load_cert(cert)


def _verify_signed_by(cert, issuer_cert):
    issuer_cert.public_key().verify(
        cert.signature,
        cert.tbs_certificate_bytes,
        padding.PKCS1v15(),
        cert.signature_hash_algorithm,
    )


def _raise_if_expired(cert):
    now = _now()
    if cert.not_valid_before_utc > now or cert.not_valid_after_utc < now:
        raise ValueError("Certificate is not currently valid")


def _serial_to_int(cert_serial):
    if isinstance(cert_serial, x509.Certificate):
        return cert_serial.serial_number
    return int(cert_serial)


def _resolve_cert_path(filename):
    path = Path(filename)
    if path.is_absolute() or path.exists():
        return path
    return CERTS_DIR / path


def _now():
    return datetime.datetime.now(datetime.timezone.utc)
