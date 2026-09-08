import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import host_delivery_v092 as transport


class GatewayNodeRuntimeTests(unittest.TestCase):
    def test_prefers_configured_gateway_node_path(self):
        with tempfile.TemporaryDirectory() as root:
            configured = Path(root) / "gateway-node.exe"
            configured.write_bytes(b"node")
            with patch.dict(os.environ, {"OPENCLAW_GATEWAY_NODE_PATH": str(configured)}, clear=False):
                self.assertEqual(transport._resolve_node_executable(), str(configured))

    def test_fails_closed_when_configured_gateway_node_path_is_missing(self):
        missing = r"C:\missing\gateway-node.exe"
        with patch.dict(os.environ, {"OPENCLAW_GATEWAY_NODE_PATH": missing}, clear=False):
            with self.assertRaisesRegex(FileNotFoundError, "OPENCLAW_GATEWAY_NODE_PATH"):
                transport._resolve_node_executable()


if __name__ == "__main__":
    unittest.main()
