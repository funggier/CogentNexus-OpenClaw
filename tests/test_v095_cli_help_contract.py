import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import cnxclaw


class V095CliHelpContractTests(unittest.TestCase):
    def test_help_exposes_canonical_readonly_check_command(self):
        text = cnxclaw.help_text()
        self.assertIn("cnxclaw.cmd check cogentnexus-openclaw", text)
        self.assertIn("Provider/model/auth/routing selection is owned by OpenClaw.", text)


if __name__ == "__main__":
    unittest.main()
