# Buoi 2 - Ma hoa va trien khai PKI

Thu muc nay gom hai bai thuc hanh:

- `crypto-toolkit`: AES-GCM, RSA signature, Argon2 password hash, CLI, Flask API, Tkinter GUI va tests.
- `mini-ca`: mo phong Certificate Authority, root CA, intermediate CA, cap chung chi, verify chain, revoke va OCSP status.

## Chay crypto-toolkit

```powershell
cd "Buoi2\crypto-toolkit"
python -m pytest -q
python -m securecrypto.cli --encrypt files\data.txt --password pass123
python -m securecrypto.cli --decrypt files\data.txt.enc --password <key-in-ra-tu-lenh-encrypt>
python -m securecrypto.api
python -m securecrypto.app_gui
```

API Flask:

- `POST http://127.0.0.1:5000/encrypt` voi form-data `file` va `password`.
- `POST http://127.0.0.1:5000/decrypt` voi form-data `file` va `password` la key base64 tra ve khi encrypt.

## Chay mini-ca

```powershell
cd "Buoi2\mini-ca"
python -m pytest -q
python demo.py
```

Chung chi va khoa sinh ra khi chay demo se nam trong `Buoi2/mini-ca/certs`.
