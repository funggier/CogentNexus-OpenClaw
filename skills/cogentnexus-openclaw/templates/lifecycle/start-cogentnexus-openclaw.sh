#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
PYTHON_BIN=${PYTHON_BIN:-python3}
RUNTIME_ROOT=${COGENTNEXUS_ROOT:-"$PWD/.cogentnexus-openclaw"}
exec "$PYTHON_BIN" "$SKILL_ROOT/scripts/runtime.py" --root "$RUNTIME_ROOT" lifecycle start --provider
