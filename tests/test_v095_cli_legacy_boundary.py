import ast
import unittest
from pathlib import Path

CNXCLAW = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "cnxclaw.py"


class V095CliLegacyBoundaryTests(unittest.TestCase):
    @staticmethod
    def _main_node():
        tree = ast.parse(CNXCLAW.read_text(encoding="utf-8"))
        return next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")

    def test_main_does_not_reference_provider_transition(self):
        calls = [
            node.func.id
            for node in ast.walk(self._main_node())
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        ]
        self.assertNotIn("provider_transition", calls)

    def test_main_does_not_reference_openclaw_route_begin(self):
        route_begin_calls = []
        for node in ast.walk(self._main_node()):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            target = node.func
            if target.attr != "begin":
                continue
            owner = target.value
            if isinstance(owner, ast.Name) and owner.id == "openclaw_route":
                route_begin_calls.append(node)
        self.assertEqual(route_begin_calls, [])

    def test_help_text_does_not_advertise_removed_cloud_command(self):
        tree = ast.parse(CNXCLAW.read_text(encoding="utf-8"))
        help_node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "help_text")
        returns = [node.value for node in ast.walk(help_node) if isinstance(node, ast.Return)]
        self.assertEqual(len(returns), 1)
        self.assertIsInstance(returns[0], ast.Constant)
        self.assertNotIn("cnxclaw.cmd cloud", returns[0].value)


if __name__ == "__main__":
    unittest.main()
