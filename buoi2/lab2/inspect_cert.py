from ca_utils import load_cert


def main():
    cert = load_cert("certs/Pham_Duy_Khanh_2387700029_cert.pem")
    print("Subject:", cert.subject.rfc4514_string())
    print("Issuer :", cert.issuer.rfc4514_string())
    print("Serial :", hex(cert.serial_number))
    print("Valid  :", cert.not_valid_before_utc.date(), "->", cert.not_valid_after_utc.date())


if __name__ == "__main__":
    main()
