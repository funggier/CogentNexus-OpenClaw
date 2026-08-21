import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import provider


class ProviderModelRouteV092Tests(unittest.TestCase):
    def test_openclaw_model_prefixes_map_to_cnx_provider_names(self):
        self.assertEqual(provider.model_provider("ollama/qwen3.5:9b"), "ollama")
        self.assertEqual(provider.model_provider("lmstudio/qwen3.5-9b"), "lmstudio")
        self.assertEqual(provider.model_provider("lmstudio_local/qwen/qwen3.5-9b"), "lmstudio")
        self.assertIsNone(provider.model_provider("openai/gpt-5"))
        self.assertIsNone(provider.model_provider(None))


if __name__ == "__main__":
    unittest.main()
