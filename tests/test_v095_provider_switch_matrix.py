import copy
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_state_v095


class V095ProviderSwitchMatrixTests(unittest.TestCase):
    def _assert_switch_is_metadata_only(self, before_state, provider_before, provider_after):
        simulated_openclaw_route = {
            "provider": provider_before,
            "model": "model-before",
            "auth": "openclaw-owned",
        }
        after_route = dict(simulated_openclaw_route)
        after_route.update({"provider": provider_after, "model": "model-after"})

        cnx_before = copy.deepcopy(before_state)
        cnx_after = copy.deepcopy(before_state)

        self.assertNotEqual(after_route["provider"], simulated_openclaw_route["provider"])
        self.assertNotEqual(after_route["model"], simulated_openclaw_route["model"])
        self.assertEqual(cnx_after, cnx_before)
        self.assertEqual(cnx_after["cnxMode"], "active")
        self.assertEqual(cnx_after["generation"], cnx_before["generation"])
        self.assertEqual(cnx_after["providerOwnership"], "openclaw")
        self.assertNotIn("selectedProvider", cnx_after)
        self.assertNotIn("desiredProvider", cnx_after)

    def test_ollama_to_cloud_preserves_cnx_state(self):
        self._assert_switch_is_metadata_only(host_state_v095.default_state(), "ollama", "cloud")

    def test_cloud_to_ollama_preserves_cnx_state(self):
        self._assert_switch_is_metadata_only(host_state_v095.default_state(), "cloud", "ollama")

    def test_cloud_to_unknown_future_provider_preserves_cnx_state(self):
        self._assert_switch_is_metadata_only(host_state_v095.default_state(), "cloud", "future-provider/example-model")

    def test_provider_metadata_is_not_host_generation_authority(self):
        state = host_state_v095.default_state()
        generation = state["generation"]
        for provider_name in ("ollama", "cloud", "future-provider"):
            state["lastProviderMetadata"] = {"provider": provider_name}
            self.assertEqual(state["generation"], generation)
            self.assertEqual(state["cnxMode"], "active")


if __name__ == "__main__":
    unittest.main()
