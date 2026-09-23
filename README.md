# TH_LT_ANTT – Bài Thực Hành An Toàn Thông Tin

**Tác giả:** KANE

Các lab về lập trình bảo mật cơ bản: validation, pre-commit hooks, logging bảo mật.

## Cấu trúc

```
├── Lab01/    SecureValidator – thư viện kiểm tra và làm sạch đầu vào
├── Lab02/    GitSecure – pre-commit hook phát hiện thông tin nhạy cảm
└── Lab03/    SecureLogger – hệ thống ghi log bảo mật tích hợp Flask
```

## Lab01 – SecureValidator

Thư viện validate và sanitize input gồm 5 hàm: `validate_email`, `validate_url`, `validate_filename`, `sanitize_sql_input`, `sanitize_html_input`.

`Exploit.md` phân tích các điểm yếu: SSRF qua URL nội bộ, SQL injection bằng toán tử `||`, XSS qua thuộc tính `href`.

| Hàm | Lỗ hổng | Bypass |
|-----|---------|--------|
| `validate_email` | Regex sai RFC | `user..name@`, thiếu `+tag` |
| `validate_url` | Không chặn IP nội bộ | SSRF qua `127.0.0.1`, `169.254.x.x` |
| `validate_filename` | Phụ thuộc thứ tự decode | URL-encode path traversal |
| `sanitize_sql_input` | Blacklist không đầy đủ | `\|\|` operator, comment injection |
| `sanitize_html_input` | Chỉ escape content | `javascript:` trong href |

## Lab02 – GitSecure Pre-commit Hook

Hook tự động chặn commit nếu phát hiện thông tin nhạy cảm (password, token, API key) hoặc file có quyền world-writable.

```bash
cd Lab02
pip install -r requirements.txt
git init && git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

| Pattern | Ví dụ bị chặn |
|---------|---------------|
| `apikey = "..."` | `apikey = "AbCdEf0123456789"` |
| `secret = "..."` | `secret = "mysecret"` |
| `password = "..."` | `password = "123456"` |
| `token = "..."` | `token = "abc1234567890"` |
| AWS Access Key | `AKIA...` |

## Lab03 – SecureLogger

Flask API `/validate` tích hợp logging bảo mật: tự động che PII, ghi JSON, nén log cũ bằng gzip, hash SHA-256 để phát hiện giả mạo log.

```bash
cd Lab03
pip install -r requirements.txt
python app.py
```

| Tấn công | Kết quả |
|----------|---------|
| XSS `<script>` | HTML-escaped → vô hiệu |
| SQL Injection `' OR 1=1` | Strip keywords → vô hiệu |
| Path Traversal `../../etc/passwd` | filename = false |
| PII trong log | Auto-masked `<email_masked>` |
| Log tampering | SHA-256 signature trong `.sig` |