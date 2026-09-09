import ast
import unittest
from pathlib import Path

CNXCLAW = Path(__file__).resolve().parents[1] / "skills" / "cogentnexus-openclaw" / "scripts" / "cnxclaw.py"


class V095CliLegacyBoundaryTests(unittest.TestCase):
    def test_main_does_not_reference_provider_transition(self):
        tree = ast.parse(CNXCLAW.read_text(encoding="utf-8"))
        main_node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
        calls = [
            node.func.id
            for node in ast.walk(main_node)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        ]
        self.assertNotIn("provider_transition", calls)

    def test_main_does_not_reference_openclaw_route_begin(self):
        tree = ast.parse(CNXCLAW.read_text(encoding="utf-8"))
        main_node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
        route_begin_calls = [
            node
            for node in ast.walk(main_node)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Attribute)
            and isinstance(node.func.value.value, ast.Name)
            and node.func.value.value.id == "openclaw_route"
            and node.func.value.attr == "begin"
            and node.func.attr == "__call__"
        ]
        self.assertEqual(route_begin_calls, [])


if __name__ == "__main__":
    unittest.main()
