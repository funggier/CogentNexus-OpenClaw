from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.manage_agents_policy import BEGIN, END, install, merge


POLICY = "## CogentNexus\n\nUse it for every request."


class ManageAgentsPolicyTests(unittest.TestCase):
    def test_append_preserves_existing_content(self):
        updated, changed = merge("# Existing\n", POLICY)
        self.assertTrue(changed)
        self.assertTrue(updated.startswith("# Existing\n"))
        self.assertEqual(updated.count(BEGIN), 1)
        self.assertEqual(updated.count(END), 1)

    def test_update_is_idempotent(self):
        first, _ = merge("# Existing\n", POLICY)
        second, changed = merge(first, POLICY)
        self.assertFalse(changed)
        self.assertEqual(second, first)

    def test_incomplete_block_fails_closed(self):
        with self.assertRaises(ValueError):
            merge(f"# Existing\n{BEGIN}\nbroken\n", POLICY)

    def test_install_backs_up_existing_agents(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            workspace.mkdir()
            agents = workspace / "AGENTS.md"
            agents.write_text("# Existing\n", encoding="utf-8")
            policy = root / "policy.md"
            policy.write_text(POLICY, encoding="utf-8")
            result = install(workspace, policy, workspace / "backups")
            self.assertTrue(result["changed"])
            self.assertEqual(Path(str(result["backup"])).read_text(encoding="utf-8"), "# Existing\n")
            self.assertIn("Use it for every request.", agents.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
