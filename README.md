# TH_LT_ANTT - Bai Thuc Hanh An Toan Thong Tin

**Tac gia:** Phạm Duy Khánh - MSSV 2387700029

Repo duoc chia theo tung buoi thuc hanh:

```text
.
├── buoi1/    Cac lab validation, GitSecure pre-commit hook, SecureLogger
├── buoi2/    Ma hoa, trien khai PKI va Certificate Authority
└── buoi3/    Bao mat Socket voi SSL/TLS, SecureChat va cong cu NetRecon
```

## Buoi1

Noi dung goc gom:

- `Lab01`: SecureValidator - thu vien kiem tra va lam sach dau vao.
- `Lab02`: GitSecure - pre-commit hook phat hien thong tin nhay cam.
- `Lab03`: SecureLogger - he thong ghi log bao mat tich hop Flask.
- `screenshots`: anh minh hoa ket qua Buoi 1.

Xem them tai [buoi1/README.md](buoi1/README.md).

## Buoi2

Noi dung moi gom:

- `crypto-toolkit`: AES-GCM, RSA signature, Argon2 password hashing, CLI, Flask API, Tkinter GUI va tests.
- `mini-ca`: tao Root CA, Intermediate CA, cap chung chi, xac thuc certificate chain, revoke certificate va OCSP status.

Xem them tai [buoi2/README.md](buoi2/README.md).

## Buoi3

Noi dung Buoi 3 gom:

- `secure-chat`: Ung dung chat bao mat su dung SSL/TLS socket (mTLS), chung chi so X.509 (Root CA, Server, Client), ma hoa dau-cuoi E2EE (AES-256-CBC, PKCS7), ConnectionManager va RoomManager da luong.
- `netrecon`: Bo cong cu trinh sat va quet mang tich hop quet cong bat dong bo (asyncio PortScanner), nhan dang dich vu voi Nmap, trich xuat Banner Grabber, so do mang ARP, kiem tra lo hong CVE (VulnChecker), giao dien Web Flask + HTMX va CLI voi Click.

Xem them tai [buoi3/README.md](buoi3/README.md).
