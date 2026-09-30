import datetime
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization


CERTS_DIR = Path(__file__).resolve().parent / "certs"
CERTS_DIR.mkdir(exist_ok=True)
CRL_FILE = CERTS_DIR / "ca_crl.pem"


def load_cert(filepath):
    path = _resolve_path(filepath)
    return x509.load_pem_x509_certificate(path.read_bytes())


def load_key(filepath):
    path = _resolve_path(filepath)
    return serialization.load_pem_private_key(path.read_bytes(), password=None)


def create_empty_crl(issuer_cert, issuer_key):
    crl = (
        x509.CertificateRevocationListBuilder()
        .issuer_name(issuer_cert.subject)
        .last_update(_now())
        .next_update(_now() + datetime.timedelta(days=7))
        .sign(private_key=issuer_key, algorithm=hashes.SHA256())
    )
    CRL_FILE.write_bytes(crl.public_bytes(serialization.Encoding.PEM))
    return crl


def revoke_certificate(cert_file, issuer_cert_file, issuer_key_file, reason=x509.ReasonFlags.key_compromise):
    cert = load_cert(cert_file)
    issuer_cert = load_cert(issuer_cert_file)
    issuer_key = load_key(issuer_key_file)

    revoked_certs = []
    if CRL_FILE.exists():
        revoked_certs = list(x509.load_pem_x509_crl(CRL_FILE.read_bytes()))

    revoked_cert = (
        x509.RevokedCertificateBuilder()
        .serial_number(cert.serial_number)
        .revocation_date(_now())
        .add_extension(x509.CRLReason(reason), critical=False)
        .build()
    )
    revoked_certs.append(revoked_cert)

    crl_builder = (
        x509.CertificateRevocationListBuilder()
        .issuer_name(issuer_cert.subject)
        .last_update(_now())
        .next_update(_now() + datetime.timedelta(days=7))
    )
    for item in revoked_certs:
        crl_builder = crl_builder.add_revoked_certificate(item)

    crl = crl_builder.sign(private_key=issuer_key, algorithm=hashes.SHA256())
    CRL_FILE.write_bytes(crl.public_bytes(serialization.Encoding.PEM))
    return crl


def check_revocation_status(cert_file):
    cert = load_cert(cert_file)
    if not CRL_FILE.exists():
        return False
    crl = x509.load_pem_x509_crl(CRL_FILE.read_bytes())
    return any(item.serial_number == cert.serial_number for item in crl)


def _resolve_path(filepath):
    path = Path(filepath)
    if path.is_absolute() or path.exists():
        return path
    return CERTS_DIR / path


def _now():
    return datetime.datetime.now(datetime.timezone.utc)
