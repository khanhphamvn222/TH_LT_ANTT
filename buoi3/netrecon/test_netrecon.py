import unittest
import asyncio
from modules.filter_utils import filter_targets
from modules.vuln_checker import check_vulns
from modules.network_mapper import map_network
from modules.port_scanner import async_scan_ports
from app import app

class TestNetRecon(unittest.TestCase):
    def test_filter_targets(self):
        ips = ["192.168.1.1", "192.168.1.2", "10.0.0.1", "127.0.0.1"]
        # Whitelist
        wl_res = filter_targets(ips, whitelist=["192.168.1.1", "127.0.0.1"])
        self.assertEqual(set(wl_res), {"192.168.1.1", "127.0.0.1"})
        # Blacklist
        bl_res = filter_targets(ips, blacklist=["10.0.0.1"])
        self.assertNotIn("10.0.0.1", bl_res)
        self.assertIn("192.168.1.1", bl_res)

    def test_vuln_checker(self):
        ports = [21, 22, 80, 9999]
        res = check_vulns(ports)
        self.assertIn(21, res)
        self.assertIn("CVE-2015-3306", res[21])
        self.assertIn(22, res)
        self.assertIn(80, res)
        self.assertNotIn(9999, res)

    def test_network_mapper(self):
        output = map_network()
        self.assertIsInstance(output, str)
        self.assertTrue(len(output) > 0)

    def test_port_scanner_mock(self):
        # Scan 127.0.0.1 for high unreachable port
        res = asyncio.run(async_scan_ports("127.0.0.1", [65534], rate_limit=10))
        self.assertIsInstance(res, str)

    def test_flask_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NetRecon", response.data)
        self.assertIn(b"Target IP", response.data)

    def test_flask_scan_vuln_mode(self):
        tester = app.test_client(self)
        response = tester.post('/scan', data={
            'target': '127.0.0.1',
            'ports': '22,80,443',
            'mode': 'vuln',
            'email': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Vulnerability Check", response.data)
        self.assertIn(b"CVE-2018-15473", response.data)

if __name__ == '__main__':
    unittest.main()
