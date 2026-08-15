import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BaselineContractTests(unittest.TestCase):
    def test_release_versions_are_synchronized(self):
        expected = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        package = json.loads((ROOT / "plugins/cogentnexus-rotation/package.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "plugins/cogentnexus-rotation/openclaw.plugin.json").read_text(encoding="utf-8"))
        lock = json.loads((ROOT / "plugins/cogentnexus-rotation/package-lock.json").read_text(encoding="utf-8"))
        self.assertEqual(expected, package["version"])
        self.assertEqual(expected, manifest["version"])
        self.assertEqual(expected, lock["version"])
        self.assertEqual(expected, lock["packages"][""]["version"])

    def test_workspace_policy_mirrors_are_identical(self):
        root_policy = (ROOT / "templates/AGENTS.cogentnexus.md").read_text(encoding="utf-8")
        skill_policy = (ROOT / "skills/cogentnexus/templates/AGENTS.cogentnexus.md").read_text(encoding="utf-8")
        self.assertEqual(root_policy, skill_policy)

    def test_policy_selects_lane_before_heavy_skill_loading(self):
        policy = (ROOT / "skills/cogentnexus/templates/AGENTS.cogentnexus.md").read_text(encoding="utf-8")
        self.assertIn("Choose the lightest reliable lane before loading heavy CogentNexus references", policy)
        self.assertIn("DIRECT conversation stays lightweight", policy)
        self.assertIn("Load the `cogentnexus` skill", policy)
        self.assertNotIn("Load and apply the `cogentnexus` skill before reasoning", policy)

    def test_skill_does_not_force_every_request_into_runtime(self):
        skill = (ROOT / "skills/cogentnexus/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Do not load heavy CogentNexus modules merely to answer an obvious DIRECT", skill)
        self.assertNotIn("Use this entry point for every request", skill)
        self.assertNotIn("Choose Direct, Verified, or Durable", skill)

    def test_canonical_baseline_and_install_guides_exist(self):
        for relative in (
            "docs/BASELINE.md",
            "docs/INSTALL.md",
            "docs/INSTALL.th.md",
            "docs/releases/v0.8.0.md",
        ):
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            self.assertTrue(path.read_text(encoding="utf-8").strip(), relative)

    def test_passthrough_invariant_is_documented(self):
        baseline = (ROOT / "docs/BASELINE.md").read_text(encoding="utf-8")
        self.assertIn("PASSTHROUGH", baseline)
        self.assertIn("OpenClaw must remain usable without CogentNexus", baseline)
        self.assertIn("must not silently disappear", baseline)


if __name__ == "__main__":
    unittest.main()
