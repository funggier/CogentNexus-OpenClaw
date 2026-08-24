from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "cogentnexus-openclaw" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "lifecycle_v092.py"
spec = importlib.util.spec_from_file_location("cnx_lifecycle_v092", SCRIPT)
cnx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cnx)


def write_payload(root: Path, version: str, bootstrap_text: str = "console.log('ok')\n", ticket_text: str = "export const ok = true;\n") -> Path:
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "dist").mkdir(parents=True, exist_ok=True)
    (root / "openclaw.plugin.json").write_text(
        json.dumps({"id": "cogentnexus-openclaw", "version": version}), encoding="utf-8"
    )
    (root / "package.json").write_text(
        json.dumps({"name": "openclaw-plugin-cogentnexus-openclaw", "version": version}),
        encoding="utf-8",
    )
    bootstrap = root / "scripts" / "bootstrap-ticket-db.mjs"
    bootstrap.write_text(bootstrap_text, encoding="utf-8")
    (root / "dist" / "ticket-store.js").write_text(ticket_text, encoding="utf-8")
    return bootstrap


def managed_package_root(state: Path, project_name: str) -> Path:
    return state / "npm" / "projects" / project_name / "node_modules" / "openclaw-plugin-cogentnexus-openclaw"


class LifecycleV092Tests(unittest.TestCase):
    def test_resolves_openclaw_managed_npm_wrapper_when_legacy_extension_is_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / ".openclaw"
            project = state / "npm" / "projects" / "openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-live"
            expected = write_payload(
                project / "node_modules" / "openclaw-plugin-cogentnexus-openclaw",
                "0.9.3",
            )
            (project / "package.json").write_text(
                json.dumps({"private": True, "dependencies": {"openclaw-plugin-cogentnexus-openclaw": "file:plugin.tgz"}}),
                encoding="utf-8",
            )

            actual = cnx.resolve_installed_bootstrap(state)

            self.assertEqual(actual.resolve(), expected.resolve())
            self.assertFalse((state / "extensions" / "cogentnexus-openclaw").exists())

    def test_accepts_exact_npm_managed_project_root_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / ".openclaw"
            managed = state / "npm" / "projects" / "direct-package-generation"
            expected = write_payload(managed, "0.9.3")

            actual = cnx.resolve_installed_bootstrap(state)
            self.assertEqual(actual.resolve(), expected.resolve())

    def test_does_not_recursively_scan_unrelated_nested_node_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / ".openclaw"
            unrelated = (
                state
                / "npm"
                / "projects"
                / "some-other-plugin"
                / "node_modules"
                / "nested-dependency"
                / "node_modules"
                / "openclaw-plugin-cogentnexus-openclaw"
            )
            write_payload(unrelated, "9.9.9")

            with self.assertRaisesRegex(RuntimeError, "no exact installed"):
                cnx.resolve_installed_bootstrap(state)

    def test_rejects_non_exact_package_versions_across_generations(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / ".openclaw"
            old_root = managed_package_root(state, "generation-old")
            new_root = managed_package_root(state, "generation-new")
            write_payload(old_root, "0.9.0", bootstrap_text="old\n", ticket_text="old-store\n")
            write_payload(new_root, "0.9.1", bootstrap_text="new\n", ticket_text="new-store\n")

            with self.assertRaisesRegex(RuntimeError, "no exact installed"):
                cnx.resolve_installed_bootstrap(state)

    def test_same_highest_version_with_conflicting_payloads_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / ".openclaw"
            first = managed_package_root(state, "generation-a")
            second = managed_package_root(state, "generation-b")
            write_payload(first, "0.9.3", bootstrap_text="a\n", ticket_text="same\n")
            write_payload(second, "0.9.3", bootstrap_text="b\n", ticket_text="same\n")

            with self.assertRaisesRegex(RuntimeError, "ambiguous"):
                cnx.resolve_installed_bootstrap(state)

    def test_same_exact_version_identical_payload_is_still_ambiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / ".openclaw"
            first = managed_package_root(state, "generation-a")
            second = managed_package_root(state, "generation-b")
            write_payload(first, "0.9.3")
            write_payload(second, "0.9.3")
            os.utime(first, ns=(1_000_000_000, 1_000_000_000))
            os.utime(second, ns=(2_000_000_000, 2_000_000_000))

            with self.assertRaisesRegex(RuntimeError, "ambiguous"):
                cnx.resolve_installed_bootstrap(state)

    def test_bootstrap_executes_verified_managed_payload_with_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / ".openclaw"
            managed = managed_package_root(state, "generation-live")
            expected = write_payload(managed, "0.9.1")
            result = subprocess.CompletedProcess([], 0, "", "")

            with (
                mock.patch.object(cnx, "resolve_installed_bootstrap", return_value=expected),
                mock.patch.object(cnx.base, "node_executable", return_value="node-test"),
                mock.patch.object(cnx.base, "run", return_value=result) as run,
            ):
                actual = cnx.bootstrap_ticket_database()

            self.assertEqual(actual, expected)
            run.assert_called_once_with(
                ["node-test", str(expected), "--workspace", str(cnx.base.WORKSPACE)],
                timeout=120,
                check=True,
            )

    def test_reset_ownership_mismatch_has_zero_state_change(self):
        with (
            tempfile.TemporaryDirectory() as tmp,
            mock.patch.object(cnx.namespace_ownership, "verify_manifest", side_effect=RuntimeError("tampered")),
            mock.patch.object(cnx.base, "confirm") as confirm,
            mock.patch.object(cnx.base, "disable_managed") as disable,
        ):
            self.assertEqual(cnx.reset(Path(tmp)), 2)
            confirm.assert_not_called()
            disable.assert_not_called()

    def test_uninstall_ownership_mismatch_has_zero_state_change(self):
        with (
            tempfile.TemporaryDirectory() as tmp,
            mock.patch.object(cnx.namespace_ownership, "verify_manifest", side_effect=RuntimeError("tampered")),
            mock.patch.object(cnx.base, "confirm") as confirm,
            mock.patch.object(cnx.base, "uninstall_plugin") as uninstall_plugin,
        ):
            self.assertEqual(cnx.uninstall(Path(tmp)), 2)
            confirm.assert_not_called()
            uninstall_plugin.assert_not_called()


if __name__ == "__main__":
    unittest.main()
