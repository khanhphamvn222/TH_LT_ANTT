---
sidebar_position: 1
---

# Bài 6: Bảo mật với DevSecOps

- **Sinh viên:** Phạm Duy Khánh
- **MSSV:** 2387700029
- **Môn học:** Thực hành Lý thuyết An toàn thông tin (TH_LT_ANTT)

## 1. Giới thiệu DevSecOps

Trong kỷ nguyên DevOps, tốc độ triển khai phần mềm cần song hành với bảo mật. DevSecOps giúp tích hợp bảo mật xuyên suốt trong pipeline CI/CD:

- **Access Control:** Kiểm soát quyền truy cập và phân quyền tối thiểu (Least Privilege).
- **Secrets Management:** Không hardcode API keys, mật khẩu; sử dụng kho bí mật chuyên dụng.
- **Security Gates:** Tích hợp các cổng kiểm tra bảo mật tự động (SAST, SCA, DAST).
- **Runner Hardening:** Bảo vệ môi trường thực thi CI/CD runner khỏi bị chiếm quyền điều khiển.
- **IaC Security:** Quét cấu hình hạ tầng dưới dạng mã (Terraform, Dockerfile, Ansible).

## 2. Quy trình CI/CD

Pipeline tự động hóa gồm 2 giai đoạn chính:
1. **Build Stage:** Biên dịch mã nguồn, cài đặt thư viện phụ thuộc và đóng gói tài nguyên tĩnh (Artifacts).
2. **Deploy Stage:** Tự động triển khai lên môi trường sản phẩm (GitHub Pages / GitLab Pages).
