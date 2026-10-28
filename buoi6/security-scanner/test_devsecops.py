#!/usr/bin/env python3
"""
Unit Tests for DevSecOps Security Tools
"""
import unittest
from secret_scanner import SecretScanner
from iac_security_scanner import IaCSecurityScanner

class TestDevSecOps(unittest.TestCase):
    def setUp(self):
        self.secret_scanner = SecretScanner()
        self.iac_scanner = IaCSecurityScanner()

    def test_detect_hardcoded_password(self):
        code = 'DB_PASSWORD = "MyPassword2026!"'
        findings = self.secret_scanner.scan_content(code, "test.py")
        self.assertGreaterEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"], "Hardcoded Password")

    def test_detect_aws_token(self):
        code = 'AWS_KEY = "AKIAIOSFODNN7EXAMPLE"'
        findings = self.secret_scanner.scan_content(code, "deploy.py")
        self.assertGreaterEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "CRITICAL")

    def test_security_gate_blocking(self):
        code = 'API_TOKEN = "ghp_123456789012345678901234567890123456"'
        findings = self.secret_scanner.scan_content(code, "config.py")
        passed = self.secret_scanner.evaluate_gate(findings, block_on="HIGH")
        self.assertFalse(passed, "Security Gate must block CRITICAL / HIGH secrets!")

    def test_iac_insecure_curl_pipe(self):
        ci_code = 'script:\n  - curl https://insecure.site/install.sh | bash'
        findings = self.iac_scanner.scan_ci_yaml(ci_code)
        self.assertGreaterEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "CRITICAL")

    def test_dockerfile_root_detection(self):
        dockerfile = 'FROM node:18\nWORKDIR /app\nCOPY . .\nCMD ["npm", "start"]'
        findings = self.iac_scanner.scan_dockerfile(dockerfile)
        rules = [f["rule"] for f in findings]
        self.assertIn("Container Running as Root", rules)

if __name__ == "__main__":
    unittest.main()
