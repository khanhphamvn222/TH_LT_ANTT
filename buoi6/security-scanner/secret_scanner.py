#!/usr/bin/env python3
"""
Secret Scanner (DevSecOps Security Gate)
Kiem tra ro ri bi mat, khoa API, mat khau trong ma nguon va file cau hinh.
Tuan thu nguyen tac Secrets Management & Secret Scanning trong CI/CD.
"""
import re
from typing import List, Dict, Any

class SecretScanner:
    """Bo kiem tra phat hien secrets va credentials hardcoded."""

    RULES = [
        {
            "name": "AWS Access Key ID",
            "regex": r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
            "severity": "CRITICAL"
        },
        {
            "name": "Generic API Key / Secret Token",
            "regex": r"(?i)(?:api_key|apikey|secret_key|secret_token|access_token|auth_token)\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{20,})['\"]",
            "severity": "HIGH"
        },
        {
            "name": "Hardcoded Password",
            "regex": r"(?i)(?:password|passwd|pwd)\s*[:=]\s*['\"]([^'\"]{6,})['\"]",
            "severity": "HIGH"
        },
        {
            "name": "Private Key Header",
            "regex": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
            "severity": "CRITICAL"
        },
        {
            "name": "GitLab / GitHub Personal Access Token",
            "regex": r"(?:glpat-[a-zA-Z0-9_\-]{20,}|ghp_[a-zA-Z0-9]{36,})",
            "severity": "CRITICAL"
        }
    ]

    def scan_content(self, content: str, filename: str = "unknown") -> List[Dict[str, Any]]:
        findings = []
        lines = content.splitlines()
        for line_no, line in enumerate(lines, 1):
            # Bo qua dong comment thong thuong neu can
            for rule in self.RULES:
                matches = re.finditer(rule["regex"], line)
                for match in matches:
                    secret_val = match.group(0)
                    # Che gia tri nhay cam khi log
                    masked_val = secret_val[:4] + "*" * (len(secret_val) - 8) + secret_val[-4:] if len(secret_val) > 8 else "***"
                    findings.append({
                        "file": filename,
                        "line": line_no,
                        "rule": rule["name"],
                        "severity": rule["severity"],
                        "snippet": line.strip(),
                        "masked_match": masked_val
                    })
        return findings

    def evaluate_gate(self, findings: List[Dict[str, Any]], block_on: str = "HIGH") -> bool:
        """Kiem tra Security Gate: Tra ve True neu vuot qua, False neu bi chan."""
        severity_rank = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        threshold = severity_rank.get(block_on, 3)
        for f in findings:
            if severity_rank.get(f["severity"], 0) >= threshold:
                return False
        return True

if __name__ == "__main__":
    scanner = SecretScanner()
    test_code = """
    # Sample config
    DB_USER = "admin"
    DB_PASSWORD = "SuperSecretPassword123!"
    API_KEY = "ak_live_abcdef1234567890abcdef"
    """
    results = scanner.scan_content(test_code, "config.py")
    print(f"Phat hien {len(results)} loi bao mat secret:")
    for r in results:
        print(f"[{r['severity']}] {r['rule']} tai dong {r['line']}: {r['masked_match']}")
    passed = scanner.evaluate_gate(results)
    print(f"Security Gate Passed: {passed}")
