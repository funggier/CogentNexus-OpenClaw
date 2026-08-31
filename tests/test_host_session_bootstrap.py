from __future__ import annotations

import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
HOST=ROOT/"skills"/"cogentnexus-openclaw"/"scripts"/"host.py"
spec=importlib.util.spec_from_file_location("cnx_host_session_bootstrap",HOST)
cnx_host=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx_host)


def completed(stdout: str):
    return subprocess.CompletedProcess(["openclaw"],0,stdout=stdout,stderr="")


class HostSessionBootstrapTests(unittest.TestCase):
    def test_empty_store_bootstraps_default_main_session_through_gateway_rpc(self):
        before='{"sessions":[],"count":0}'
        after='{"sessions":[{"key":"agent:main:main"}],"count":1}'
        with patch.object(cnx_host,"gateway_status",return_value={"healthy":True}), \
             patch.object(cnx_host,"default_agent_id",return_value="main"), \
             patch.object(cnx_host,"configured_main_key",return_value="main"), \
             patch.object(cnx_host,"openclaw_executable",return_value="openclaw"), \
             patch.object(cnx_host,"run",side_effect=[completed(before),completed(after)]), \
             patch.object(cnx_host,"gateway_rpc",return_value={"key":"agent:main:main"}) as rpc:
            result=cnx_host.reconcile_default_session()
        self.assertTrue(result["ok"])
        self.assertTrue(result["created"])
        self.assertEqual(result["sessionKey"],"agent:main:main")
        rpc.assert_called_once_with("sessions.create",{"key":"main","agentId":"main"},timeout=30)

    def test_existing_default_main_session_is_idempotent(self):
        existing='{"sessions":[{"key":"agent:main:main"}],"count":1}'
        with patch.object(cnx_host,"gateway_status",return_value={"healthy":True}), \
             patch.object(cnx_host,"default_agent_id",return_value="main"), \
             patch.object(cnx_host,"configured_main_key",return_value="main"), \
             patch.object(cnx_host,"openclaw_executable",return_value="openclaw"), \
             patch.object(cnx_host,"run",return_value=completed(existing)), \
             patch.object(cnx_host,"gateway_rpc") as rpc:
            result=cnx_host.reconcile_default_session()
        self.assertTrue(result["ok"])
        self.assertFalse(result["created"])
        rpc.assert_not_called()

    def test_unhealthy_gateway_does_not_mutate_sessions(self):
        with patch.object(cnx_host,"gateway_status",return_value={"healthy":False}), patch.object(cnx_host,"gateway_rpc") as rpc:
            result=cnx_host.reconcile_default_session()
        self.assertTrue(result["skipped"])
        rpc.assert_not_called()


if __name__=="__main__":
    unittest.main()
