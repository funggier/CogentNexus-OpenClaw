#!/usr/bin/env python3
"""Remove load paths that resolve to a selected OpenClaw plugin id."""

import argparse
import json
import sys
from pathlib import Path


def plugin_id(path: Path) -> str | None:
    manifest = path / "openclaw.plugin.json"
    try:
        return json.loads(manifest.read_text(encoding="utf-8")).get("id")
    except (OSError, ValueError, AttributeError):
        return path.name if path.name else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-id", required=True)
    args = parser.parse_args()
    paths = json.load(sys.stdin)
    if not isinstance(paths, list) or not all(isinstance(item, str) for item in paths):
        raise SystemExit("plugin load paths must be a JSON string array")
    filtered = [item for item in paths if plugin_id(Path(item)) != args.plugin_id]
    print(json.dumps(filtered, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
