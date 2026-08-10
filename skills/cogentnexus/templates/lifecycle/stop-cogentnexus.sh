#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
PYTHON_BIN=${PYTHON_BIN:-python3}
RUNTIME_ROOT=${COGENTNEXUS_ROOT:-"$PWD/.cogent"}
exec "$PYTHON_BIN" "$SKILL_ROOT/scripts/phase3.py" --root "$RUNTIME_ROOT" lifecycle stop --provider --reason "planned host shutdown" --owner "portable-launcher"
