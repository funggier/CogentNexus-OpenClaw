#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
WORKSPACE=${OPENCLAW_WORKSPACE:-"$HOME/.openclaw/workspace"}
SKIP_PLUGIN=0
SKIP_GATEWAY_RESTART=0
LINK_PLUGIN=0
SKIP_AGENTS_POLICY=0
VERSION=$(cat "$REPO_ROOT/VERSION" 2>/dev/null || printf 'unknown')

usage() { echo "Usage: $0 [--workspace PATH] [--skip-plugin] [--skip-gateway-restart] [--skip-agents-policy] [--link-plugin]"; }

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workspace) [ "$#" -ge 2 ] || { usage; exit 2; }; WORKSPACE=$2; shift 2 ;;
    --skip-plugin) SKIP_PLUGIN=1; shift ;;
    --skip-gateway-restart) SKIP_GATEWAY_RESTART=1; shift ;;
    --skip-agents-policy) SKIP_AGENTS_POLICY=1; shift ;;
    --link-plugin) LINK_PLUGIN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage; exit 2 ;;
  esac
done

echo "Installing CogentNexus v$VERSION"

for command_name in python openclaw; do
  command -v "$command_name" >/dev/null 2>&1 || { echo "Required command not found: $command_name" >&2; exit 1; }
done
if [ "$SKIP_PLUGIN" -eq 0 ]; then
  for command_name in node npm; do
    command -v "$command_name" >/dev/null 2>&1 || { echo "Required command not found: $command_name" >&2; exit 1; }
  done
fi
python -c "import yaml" >/dev/null 2>&1 || {
  echo "PyYAML is required. Run: python -m pip install 'PyYAML>=6.0,<7'" >&2
  exit 1
}

SOURCE_SKILL="$REPO_ROOT/skills/cogentnexus"
TARGET_SKILL="$WORKSPACE/skills/cogentnexus"
STAGED_SKILL="$WORKSPACE/.cogent/install-staging/cogentnexus"
BACKUP_ROOT="$WORKSPACE/.cogent/install-backups"
HOST_SCRIPT="$TARGET_SKILL/scripts/host_v091.py"
HOST_CONTROL_SCRIPT="$TARGET_SKILL/scripts/host_control_v091.py"
COGENT_ROOT="$WORKSPACE/.cogent"

mkdir -p "$WORKSPACE/skills"
if [ -d "$TARGET_SKILL" ]; then
  mkdir -p "$BACKUP_ROOT"
  BACKUP="$BACKUP_ROOT/cogentnexus-$(date +%Y%m%d-%H%M%S)"
  cp -R "$TARGET_SKILL" "$BACKUP"
  echo "Backed up existing skill to $BACKUP"
fi

rm -rf "$STAGED_SKILL"
mkdir -p "$(dirname "$STAGED_SKILL")"
cp -R "$SOURCE_SKILL" "$STAGED_SKILL"
rm -rf "$TARGET_SKILL"
mv "$STAGED_SKILL" "$TARGET_SKILL"
echo "Installed CogentNexus skill to $TARGET_SKILL"

python "$TARGET_SKILL/scripts/validate.py"

# v0.9.1 fresh initialization is PASSTHROUGH. MANAGED is committed only after
# the transactional Host enable sequence verifies every activation stage.
python "$HOST_SCRIPT" --root "$COGENT_ROOT" init

if [ "$SKIP_GATEWAY_RESTART" -eq 1 ]; then
  mode=$(python - "$COGENT_ROOT/host/controller.json" <<'PY'
import json,sys
from pathlib import Path
path=Path(sys.argv[1])
try:
    print(json.loads(path.read_text(encoding='utf-8')).get('mode',''))
except Exception:
    print('')
PY
)
  if [ "$mode" != "passthrough" ]; then
    echo "--skip-gateway-restart safe staging requires CogentNexus PASSTHROUGH mode. Run 'cnx disable' before staging an upgrade." >&2
    exit 1
  fi
fi

# Transactional enable reapplies the registered policy before committing
# MANAGED; in PASSTHROUGH this command is intentionally a no-op.
if [ "$SKIP_AGENTS_POLICY" -eq 0 ]; then
  python "$HOST_SCRIPT" --root "$COGENT_ROOT" policy apply
fi

if [ "$SKIP_PLUGIN" -eq 0 ]; then
  (
    cd "$REPO_ROOT/plugins/cogentnexus-rotation"
    npm ci
    npm run plugin:validate
    if [ "$LINK_PLUGIN" -eq 1 ]; then
      openclaw plugins install --link . --force
    else
      if current_paths=$(openclaw config get plugins.load.paths 2>/dev/null); then
        filtered_paths=$(printf '%s' "$current_paths" | python "$REPO_ROOT/scripts/filter_plugin_paths.py" --plugin-id cogentnexus-rotation)
        openclaw config set plugins.load.paths "$filtered_paths" --strict-json --replace
      fi
      openclaw plugins install . --force
    fi

    # Plugin code installation can restart the managed Gateway natively. Leave
    # CNX disabled until the transactional Host enable stages valid config.
    openclaw plugins disable cogentnexus-rotation
  )
fi

LAUNCHER="$WORKSPACE/cnx"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env sh
exec python "$HOST_CONTROL_SCRIPT" --root "$COGENT_ROOT" "\$@"
EOF
chmod +x "$LAUNCHER"
echo "Installed Host Controller launcher to $LAUNCHER"

if [ "$SKIP_GATEWAY_RESTART" -eq 0 ]; then
  python "$HOST_CONTROL_SCRIPT" --root "$COGENT_ROOT" enable
else
  echo "Skipped Host enable because --skip-gateway-restart was requested."
  echo "Note: OpenClaw plugin installation itself may have restarted Gateway as part of its native plugin lifecycle."
  echo "CogentNexus remains PASSTHROUGH with its plugin disabled. Run '$LAUNCHER enable' when ready."
fi

openclaw gateway status || [ "$SKIP_GATEWAY_RESTART" -eq 1 ]
python "$TARGET_SKILL/scripts/runtime.py" supervisor doctor
python "$HOST_SCRIPT" --root "$COGENT_ROOT" status

echo "CogentNexus v$VERSION installation completed successfully."
echo "Control it with: $LAUNCHER status|start|stop|restart|gateway|ticket|session|policy|disable|enable"
