#!/usr/bin/env python3
"""Task CNX-20260825-064 — executable Windows runtime-authority integration tests.

Replaces Task 063's source-string tests with real execution contracts:
T1 exact product-root contract; T2 real temp provisioning; T3 startup
fail-closed without executor-venv fallback; T4 task definition uses owned
pythonw; T5 launcher contract executes the owned interpreter; T6 normal CLI
import capability under the owned runtime; T7 no-console spawn semantics;
T8 uninstall/reset/install-over deletion-boundary semantics.
"""
from __future__ import annotations

import importlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SCRIPTS = REPO / "skills" / "cogentnexus-openclaw" / "scripts"
INSTALLER = REPO / "scripts" / "install.ps1"
sys.path.insert(0, str(SCRIPTS))

runtime_authority = importlib.import_module("runtime_authority")

IS_WINDOWS = os.name == "nt"


class TempAppDataTestCase(unittest.TestCase):
    """Base: temp LOCALAPPDATA base outside the live product root."""

    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp(prefix="cnx064-"))
        self.local_base = self._tmp / "Local"
        self.local_base.mkdir(parents=True, exist_ok=True)
        self.env = {"LOCALAPPDATA": str(self.local_base)}

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)


def _load_startup():
    spec = importlib.util.spec_from_file_location("cnx_startup", SCRIPTS / "startup.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _patched_env(local_base: Path):
    return unittest.mock.patch.dict(os.environ, {"LOCALAPPDATA": str(local_base)})


def _patched_executable(path: str):
    return unittest.mock.patch.object(runtime_authority.sys, "executable", path)


class TestExactProductRootContract(TempAppDataTestCase):
    """T1 — environment-derived vs explicit exact-product-root APIs agree exactly."""

    def test_env_derived_root_is_exact_product_dir(self):
        root = runtime_authority.app_data_root(self.env)
        self.assertEqual(root, self.local_base / "CogentNexus-OpenClaw")
        self.assertNotIn("CogentNexus-OpenClaw\\CogentNexus-OpenClaw", str(root))

    def test_runtime_root_from_application_data_exact(self):
        exact = self.local_base / "CogentNexus-OpenClaw"
        rt = runtime_authority.runtime_root_from_application_data(exact)
        self.assertEqual(rt, exact / "runtime" / "python")

    def test_explicit_form_matches_env_derived_form(self):
        derived = runtime_authority.runtime_root(env=self.env)
        explicit = runtime_authority.runtime_root_from_application_data(
            runtime_authority.app_data_root(self.env)
        )
        self.assertEqual(derived, explicit)

    def test_cli_explicit_app_root_does_not_duplicate_product_dir(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "runtime_authority.py"), "show",
             "--application-data-root", str(self.local_base / "CogentNexus-OpenClaw")],
            capture_output=True, text=True, timeout=60,
            creationflags=runtime_authority.creation_flags(),
        )
        combined = result.stdout + result.stderr
        self.assertNotIn("CogentNexus-OpenClaw\\CogentNexus-OpenClaw", combined,
                         "CLI must treat --application-data-root as the exact product root")

    def test_manifest_validation_rejects_sibling_boundary_names(self):
        evil = self.local_base / "CogentNexus-OpenClaw-evil"
        bad_manifest = {
            "runtimeRoot": str(evil / "runtime" / "python"),
            "foregroundInterpreter": str(evil / "runtime" / "python" / "Scripts" / "python.exe"),
            "backgroundInterpreter": str(evil / "runtime" / "python" / "Scripts" / "pythonw.exe"),
        }
        self.assertFalse(runtime_authority.validate_runtime(bad_manifest))


@unittest.skipUnless(IS_WINDOWS, "real provisioning integration is Windows-specific")
class TestRealTempProvisioning(TempAppDataTestCase):
    """T2 — provision a real owned runtime under a temp exact product root."""

    def test_real_provisioning_produces_valid_interpreters_and_manifest(self):
        app_root = self.local_base / "CogentNexus-OpenClaw"
        manifest = runtime_authority.ensure_runtime(application_data_root=app_root)
        rt = Path(manifest["runtimeRoot"])
        self.assertEqual(rt, app_root / "runtime" / "python")
        fg = Path(manifest["foregroundInterpreter"])
        bg = Path(manifest["backgroundInterpreter"])
        self.assertTrue(fg.is_file(), fg)
        self.assertTrue(bg.is_file(), bg)
        # ancestry: both interpreters under the exact product root
        for interp in (fg, bg):
            self.assertEqual(Path(interp).resolve().parents[3], app_root.resolve())
        # manifest base interpreter must not be this test's executor venv
        if getattr(sys, "base_prefix", sys.prefix) != sys.prefix:
            self.assertNotEqual(Path(manifest["baseInterpreter"]).resolve(), Path(sys.executable).resolve())
        # foreground stdlib probe
        probe = subprocess.run([str(fg), "-c", "import json,sys;print(json.dumps(sys.version_info[:3]))"],
                               capture_output=True, text=True, timeout=60)
        self.assertEqual(probe.returncode, 0)
        # background exit-only sentinel probe (no console stdio assumption)
        sentinel = self._tmp / "bg-sentinel.txt"
        probe_bg = subprocess.run(
            [str(bg), "-c", f"open(r'{sentinel}','w').write('ok')"],
            capture_output=True, text=True, timeout=60,
            creationflags=runtime_authority.creation_flags(),
        )
        self.assertEqual(probe_bg.returncode, 0, probe_bg.stderr)
        self.assertTrue(sentinel.exists())
        self.assertTrue(runtime_authority.validate_runtime(manifest, app_root))


@unittest.skipUnless(IS_WINDOWS, "Windows startup registration semantics")
class TestStartupFailClosed(TempAppDataTestCase):
    """T3/T4 — startup selection fails closed and never persists an executor venv."""

    def test_missing_runtime_raises_instead_of_sys_executable_fallback(self):
        startup = _load_startup()
        with _patched_executable("X:\\executor\\venv\\Scripts\\python.exe"), \
             _patched_env(self.local_base):
            with self.assertRaises(runtime_authority.RuntimeProvisioningError):
                startup.python_background()

    def test_task_definition_uses_owned_pythonw(self):
        startup = _load_startup()
        app_root = self.local_base / "CogentNexus-OpenClaw"
        manifest = runtime_authority.ensure_runtime(application_data_root=app_root)
        with _patched_executable("X:\\executor\\venv\\Scripts\\python.exe"), \
             _patched_env(self.local_base):
            selected = startup.python_background()
        self.assertEqual(Path(selected), Path(manifest["backgroundInterpreter"]))
        self.assertIn("executor", "X:\\executor\\venv", "fixture sanity")
        self.assertNotIn("executor", str(selected))

    def test_windows_task_xml_replacement_fails_closed_without_runtime(self):
        """win_enable must fail before any task XML write when the runtime is absent."""
        startup = _load_startup()
        calls = {"created": False}
        real_write = Path.write_text

        def guarded_write(self, data, *a, **k):
            if self.suffix == ".xml":
                calls["created"] = True
            return real_write(self, data, *a, **k)

        with unittest.mock.patch.object(Path, "write_text", guarded_write), \
             _patched_executable("X:\\executor\\venv\\Scripts\\python.exe"), \
             _patched_env(self.local_base):
            with self.assertRaises(RuntimeError):
                startup.win_enable(self.local_base / "CogentNexus-OpenClaw")
        self.assertFalse(calls["created"], "no task XML may be written when the owned runtime is missing")


@unittest.skipUnless(IS_WINDOWS, "launcher execution contract is Windows-specific")
class TestLauncherExecutableContract(TempAppDataTestCase):
    """T5 — generated launcher command line invokes the owned foreground interpreter."""

    def test_launcher_line_uses_owned_interpreter_and_runs_it(self):
        app_root = self.local_base / "CogentNexus-OpenClaw"
        manifest = runtime_authority.ensure_runtime(application_data_root=app_root)
        owned_fg = Path(manifest["foregroundInterpreter"])

        # Render the exact launcher line install.ps1 generates (same shape).
        cli_script = SCRIPTS / "cnxclaw_v093.py"
        marker_script = self._tmp / "marker.py"
        marker_script.write_text("import sys;print(sys.executable)\n", encoding="utf-8")
        launcher = self._tmp / "cnxclaw.cmd"
        escaped_marker = str(marker_script).replace('"', '""')
        launcher_text = (
            "@echo off\r\n"
            f'"{owned_fg}" "{escaped_marker}" %*\r\n'
            "exit /b %ERRORLEVEL%\r\n"
        )
        launcher.write_text(launcher_text, encoding="utf-8", newline="")

        result = subprocess.run([str(launcher)], capture_output=True, text=True, timeout=60)
        observed = result.stdout.strip()
        self.assertTrue(observed, result.stderr)
        self.assertEqual(Path(observed).resolve(), owned_fg.resolve(),
                         "launcher must execute the owned foreground interpreter")

        # installer source interpolates $ownedPython into the launcher text
        ps_source = INSTALLER.read_text(encoding="utf-8")
        first_launcher_line = ps_source[ps_source.index("$launcherText ="):].splitlines()[0]
        self.assertIn("$ownedPython", first_launcher_line)
        self.assertNotIn("python `\"", first_launcher_line)


class TestOwnedRuntimeRunsProductCli(TempAppDataTestCase):
    """T6 — normal non-mutating CLI entry works under the owned runtime (stdlib-only)."""

    @unittest.skipUnless(IS_WINDOWS, "provisioning integration is Windows-specific")
    def test_owned_interpreter_imports_normal_cli_surface(self):
        manifest = runtime_authority.ensure_runtime(
            application_data_root=self.local_base / "CogentNexus-OpenClaw"
        )
        fg = manifest["foregroundInterpreter"]
        probe = subprocess.run(
            [fg, "-c",
             "import sys;sys.path.insert(0,r'" + str(SCRIPTS) + "');"
             "import cnxclaw_v093;"
             "print('cli-import-ok')"],
            capture_output=True, text=True, timeout=120,
            creationflags=runtime_authority.creation_flags(),
        )
        self.assertEqual(probe.returncode, 0, probe.stderr[-500:])
        self.assertIn("cli-import-ok", probe.stdout)


class TestNoConsoleSemantics(unittest.TestCase):
    """T7 — every Windows spawn helper on the healthy supervisor path applies CREATE_NO_WINDOW."""

    def test_supervisor_spawn_helpers_use_no_window(self):
        for module_name in ("host_control", "cnxclaw"):
            module = importlib.import_module(module_name)
            flags = module.creation_flags()
            if IS_WINDOWS:
                self.assertEqual(flags & subprocess.CREATE_NO_WINDOW, subprocess.CREATE_NO_WINDOW, module_name)
        runtime_module = importlib.import_module("runtime")
        options = runtime_module.background_options()
        if IS_WINDOWS:
            self.assertEqual(
                options.get("creationflags", 0) & subprocess.CREATE_NO_WINDOW,
                subprocess.CREATE_NO_WINDOW,
            )


class TestUninstallResetInstallOverBoundary(TempAppDataTestCase):
    """T8 — the owned runtime stays inside existing application-data deletion authority."""

    def test_runtime_is_inside_app_data_deletion_boundary(self):
        app_root = self.local_base / "CogentNexus-OpenClaw"
        rt = runtime_authority.runtime_root_from_application_data(app_root)
        # runtime root resolves strictly under the product root that uninstall owns
        self.assertTrue(rt.resolve().is_relative_to(app_root.resolve()))
        # and cannot escape to a foreign location
        foreign = Path("X:/somewhere/python")
        self.assertFalse(foreign.is_relative_to(app_root))
        # validate_runtime rejects manifests pointing outside the boundary
        bad = {
            "runtimeRoot": str(foreign),
            "foregroundInterpreter": str(foreign / "Scripts" / "python.exe"),
            "backgroundInterpreter": str(foreign / "Scripts" / "pythonw.exe"),
        }
        self.assertFalse(runtime_authority.validate_runtime(bad, app_root))

    def test_install_over_validates_then_recreates_missing_runtime(self):
        app_root = self.local_base / "CogentNexus-OpenClaw"
        m1 = runtime_authority.ensure_runtime(application_data_root=app_root)
        # corrupt the manifest -> install-over validation fails -> recreate deterministically
        (Path(m1["runtimeRoot"]) / runtime_authority.MANIFEST_NAME).unlink()
        self.assertIsNone(runtime_authority.provisioned_manifest(app_root))
        m2 = runtime_authority.ensure_runtime(application_data_root=app_root)
        self.assertTrue(runtime_authority.validate_runtime(m2, app_root))
        self.assertEqual(Path(m2["runtimeRoot"]), Path(m1["runtimeRoot"]))


if __name__ == "__main__":
    unittest.main()
