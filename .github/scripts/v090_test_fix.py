from pathlib import Path

p = Path('tests/test_host_controller.py')
s = p.read_text(encoding='utf-8')
old = '''    def test_gateway_status_requires_connectivity_not_only_zero_exit(self):
        original = cnx_host.run
        try:
            cnx_host.run = lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, "Runtime: stopped\\n", "Connectivity probe: failed\\n")
            self.assertFalse(cnx_host.gateway_status()["healthy"])
            cnx_host.run = lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, "Runtime: running\\nConnectivity probe: ok\\n", "")
            self.assertTrue(cnx_host.gateway_status()["healthy"])
        finally:
            cnx_host.run = original
'''
new = '''    def test_gateway_status_requires_connectivity_not_only_zero_exit(self):
        original_run = cnx_host.run
        original_executable = cnx_host.openclaw_executable
        try:
            cnx_host.openclaw_executable = lambda: "openclaw"
            cnx_host.run = lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, "Runtime: stopped\\n", "Connectivity probe: failed\\n")
            self.assertFalse(cnx_host.gateway_status()["healthy"])
            cnx_host.run = lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, "Runtime: running\\nConnectivity probe: ok\\n", "")
            self.assertTrue(cnx_host.gateway_status()["healthy"])
        finally:
            cnx_host.run = original_run
            cnx_host.openclaw_executable = original_executable
'''
if old not in s:
    raise SystemExit('gateway health test block not found')
p.write_text(s.replace(old, new, 1), encoding='utf-8')
