# TH_LT_ANTT - Bài Thực Hành An Toàn Thông Tin

**Tác giả:** Phạm Duy Khánh - MSSV 2387700029

Repo được chia theo từng buổi thực hành:

```text
.
├── buoi1/    Các lab validation, GitSecure pre-commit hook, SecureLogger
├── buoi2/    Mã hóa, triển khai PKI và Certificate Authority
├── buoi3/    Bảo mật Socket với SSL/TLS, SecureChat và công cụ NetRecon
└── buoi4/    Bảo mật Web App và API: WebVulnScanner và bộ công cụ JWTSecure
```

## Buoi1

Nội dung gốc gồm:

- `Lab01`: SecureValidator - thư viện kiểm tra và làm sạch đầu vào.
- `Lab02`: GitSecure - pre-commit hook phát hiện thông tin nhạy cảm.
- `Lab03`: SecureLogger - hệ thống ghi log bảo mật tích hợp Flask.
- `screenshots`: ảnh minh họa kết quả Buổi 1.

Xem thêm tại [buoi1/README.md](buoi1/README.md).

## Buoi2

Nội dung gồm:

- `crypto-toolkit`: AES-GCM, RSA signature, Argon2 password hashing, CLI, Flask API, Tkinter GUI và tests.
- `mini-ca`: tạo Root CA, Intermediate CA, cấp chứng chỉ, xác thực certificate chain, revoke certificate và OCSP status.
- `images`: toàn bộ ảnh chụp minh chứng thực nghiệm Buổi 2.

Xem thêm tại [buoi2/README.md](buoi2/README.md).

## Buoi3

Nội dung Buổi 3 gồm:

- `secure-chat`: Ứng dụng chat bảo mật sử dụng SSL/TLS socket (mTLS), chứng chỉ số X.509 (Root CA, Server, Client), mã hóa đầu-cuối E2EE (AES-256-CBC, PKCS7), ConnectionManager và RoomManager đa luồng.
- `netrecon`: Bộ công cụ trinh sát và quét mạng tích hợp quét cổng bất đồng bộ (asyncio PortScanner), nhận dạng dịch vụ với Nmap, trích xuất Banner Grabber, sơ đồ mạng ARP, kiểm tra lỗ hổng CVE (VulnChecker), giao diện Web Flask + HTMX và CLI với Click.
- `images`: toàn bộ ảnh chụp minh chứng thực nghiệm Buổi 3.

Xem thêm tại [buoi3/README.md](buoi3/README.md).

## Buoi4

Nội dung Buổi 4 gồm:

- `web-vuln-scanner`: Bộ công cụ quét lỗ hổng ứng dụng Web tự động phát hiện Cross-Site Scripting (XSS), SQL Injection (SQLi), Cross-Site Request Forgery (CSRF), Server-Side Request Forgery (SSRF), tích hợp bộ sinh báo cáo tự động và giao diện Web UI Flask.
- `jwt-security-tools`: Bộ công cụ bảo mật Web API toàn diện với JWT & OAuth 2.0 gồm JWTValidator, JWTCracker đa luồng, OAuthClient (Authorization Code flow), TokenManager quản lý Access/Refresh Token và cổng APIGateway xác thực Bearer token.
- `images`: toàn bộ 13 ảnh chụp minh chứng quá trình thực hành và kiểm thử Buổi 4 (trích xuất từ báo cáo Doc1.docx).

Xem thêm tại [buoi4/README.md](buoi4/README.md).

## Buoi5

Nội dung Buổi 5 gồm:

- sast-tool: Bộ công cụ kiểm thử bảo mật tĩnh dựa trên phân tích cây cú pháp trừu tượng (AST Analyzer), kiểm tra chất lượng mã nguồn (Code Quality Checker), bộ quy tắc an ninh (Security Rule Engine), nhận diện mẫu mã độc (Vuln Pattern Matcher) và xuất báo cáo chuẩn quốc tế SARIF (Static Analysis Results Interchange Format).
- dast-tool: Bộ công cụ kiểm thử bảo mật động trong thời gian thực thi (Runtime Security Testing & Sandbox Analysis) gồm Runtime Monitor theo dõi CPU/RAM/Handles, Memory Analyzer phát hiện rò rỉ và tràn bộ đệm, Network Traffic Analyzer, Security Behavior Checker kiểm soát lời gọi hệ thống độc hại, Virtual Sandbox cô lập mã không tin cậy và máy chủ Flask REST API giám sát.
- images: toàn bộ 15 ảnh chụp minh chứng thực nghiệm xuyên suốt quá trình thực hành và kiểm thử Buổi 5.

Xem thêm tại [buoi5/README.md](buoi5/README.md).
