#!/usr/bin/env python3
"""Report the exact installable plugin payload-v2 identity without mutation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import namespace_ownership as ownership


def payload_identity(plugin_root: Path, *, expected_version: str) -> dict[str, object]:
    payload = ownership._plugin_payload(
        plugin_root.resolve(strict=False),
        expected_version=expected_version,
    )
    if payload is None:
        raise RuntimeError(
            "source plugin payload is incomplete or has the wrong id/package/version"
        )
    return {
        "version": payload["version"],
        "fingerprint": payload["fingerprint"],
        "fileCount": len(payload["files"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-root", type=Path, required=True)
    parser.add_argument("--version", default=ownership.INSTALLED_VERSION)
    args = parser.parse_args()
    try:
        result = payload_identity(args.plugin_root, expected_version=args.version)
    except RuntimeError as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
