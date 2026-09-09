import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import cnxclaw


class V095CliOwnershipTests(unittest.TestCase):
    def test_cnx_lifecycle_commands_do_not_select_or_route_provider(self):
        for command in ("start", "stop", "restart", "status"):
            with self.subTest(command=command), \
                 mock.patch.object(cnxclaw, "provider_transition") as transition, \
                 mock.patch.object(cnxclaw.openclaw_route, "begin") as route_begin, \
                 mock.patch.object(cnxclaw, "provider_snapshot", return_value={"authority": "openclaw", "providerMetadata": {}}):
                if command == "status":
                    with mock.patch.object(cnxclaw, "run_host", return_value={"ok": True, "output": {}}):
                        code = cnxclaw.main([command])
                else:
                    with mock.patch.object(cnxclaw, "delegate", return_value=0):
                        code = cnxclaw.main([command])
                self.assertEqual(code, 0)
                transition.assert_not_called()
                route_begin.assert_not_called()

    def test_local_ollama_commands_use_local_adapter_and_never_route_openclaw(self):
        with mock.patch.object(cnxclaw, "local_adapter") as adapter, mock.patch.object(cnxclaw.openclaw_route, "begin") as route_begin:
            adapter.run.return_value = (0, {"result": "ok"})
            code = cnxclaw.main(["local", "ollama", "start"])
        self.assertEqual(code, 0)
        adapter.run.assert_called_once()
        route_begin.assert_not_called()

    def test_legacy_provider_option_is_rejected_for_cnx_lifecycle(self):
        for command in ("start", "restart", "stop", "status"):
            with self.subTest(command=command):
                with mock.patch.object(cnxclaw, "provider_transition") as transition:
                    code = cnxclaw.main([command, "--provider", "ollama"])
                self.assertEqual(code, 2)
                transition.assert_not_called()

    def test_cloud_is_not_a_provider_routing_command(self):
        with mock.patch.object(cnxclaw, "provider_transition") as transition:
            code = cnxclaw.main(["cloud"])
        self.assertEqual(code, 0)
        transition.assert_not_called()


if __name__ == "__main__":
    unittest.main()
