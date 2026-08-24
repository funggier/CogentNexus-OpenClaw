#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
WORKSPACE=${OPENCLAW_WORKSPACE:-"$HOME/.openclaw/workspace"}
PROVIDER="ollama"
SKIP_PLUGIN=0
SKIP_GATEWAY_RESTART=0
LINK_PLUGIN=0
SKIP_AGENTS_POLICY=0
VERSION=$(cat "$REPO_ROOT/VERSION" 2>/dev/null || printf 'unknown')

usage() { echo "Usage: $0 [--workspace PATH] [--provider ollama] [--skip-plugin] [--skip-gateway-restart] [--skip-agents-policy] [--link-plugin]"; }

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workspace) [ "$#" -ge 2 ] || { usage; exit 2; }; WORKSPACE=$2; shift 2 ;;
    --provider)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      PROVIDER=$2
      case "$PROVIDER" in ollama) ;; *) echo "Unsupported provider in CogentNexus-OpenClaw v0.9.3: $PROVIDER (only ollama is supported)" >&2; exit 2 ;; esac
      shift 2 ;;
    --skip-plugin) SKIP_PLUGIN=1; shift ;;
    --skip-gateway-restart) SKIP_GATEWAY_RESTART=1; shift ;;
    --skip-agents-policy) SKIP_AGENTS_POLICY=1; shift ;;
    --link-plugin) LINK_PLUGIN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage; exit 2 ;;
  esac
done

echo "Installing CogentNexus-OpenClaw v$VERSION (Ollama-only)"
echo "Provider: ollama"

if { [ "$SKIP_PLUGIN" -eq 1 ] || [ "$SKIP_AGENTS_POLICY" -eq 1 ]; } && [ "$SKIP_GATEWAY_RESTART" -eq 0 ]; then
  echo "--skip-plugin and --skip-agents-policy are staging-only options. Use them with --skip-gateway-restart." >&2
  exit 2
fi

for command_name in python openclaw ollama; do
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

SOURCE_SKILL="$REPO_ROOT/skills/cogentnexus-openclaw"
TARGET_SKILL="$WORKSPACE/skills/cogentnexus-openclaw"
STAGED_SKILL="$WORKSPACE/.cogentnexus-openclaw/install-staging/cogentnexus-openclaw"
BACKUP_ROOT="$WORKSPACE/.cogentnexus-openclaw/install-backups"
HOST_SCRIPT="$TARGET_SKILL/scripts/host_v091.py"
CLI_SCRIPT="$TARGET_SKILL/scripts/cnxclaw_v093.py"
COGENT_ROOT="$WORKSPACE/.cogentnexus-openclaw"
CONTROLLER_PATH="$COGENT_ROOT/host/controller.json"
EXISTING_LAUNCHER="$WORKSPACE/cnxclaw"
OWNERSHIP_SCRIPT="$SOURCE_SKILL/scripts/namespace_ownership.py"
MIGRATION_SOURCE=""

if [ -d "$COGENT_ROOT" ]; then
  python "$OWNERSHIP_SCRIPT" verify --root "$COGENT_ROOT" --workspace "$WORKSPACE" >/dev/null
else
  LEGACY_PROOF=$(python "$OWNERSHIP_SCRIPT" inventory-legacy --workspace "$WORKSPACE")
  MIGRATION_SOURCE=$(printf '%s' "$LEGACY_PROOF" | python -c 'import json,sys; x=json.load(sys.stdin); print("legacy-cogentnexus-pre-v0.9.3" if x["mode"] == "legacy" else "")')
  if [ -n "$MIGRATION_SOURCE" ]; then
    CONTROLLER_PATH="$WORKSPACE/.cogent/host/controller.json"
    EXISTING_LAUNCHER="$WORKSPACE/cnx"
  fi
fi

read_existing_mode() {
  [ -f "$CONTROLLER_PATH" ] || { printf '%s' ''; return 0; }
  python - "$CONTROLLER_PATH" <<'PY'
import json,sys
from pathlib import Path
path=Path(sys.argv[1])
try:
    value=json.loads(path.read_text(encoding='utf-8'))
except Exception as error:
    raise SystemExit(f"Existing CogentNexus-OpenClaw controller is unreadable; refusing install mutation: {error}")
mode=value.get('mode') if isinstance(value,dict) else None
if not isinstance(mode,str) or not mode.strip():
    raise SystemExit("Existing CogentNexus-OpenClaw controller has no mode; refusing install mutation.")
print(mode)
PY
}

# Upgrade handoff is deliberately performed by the old installed launcher so a
# v0.9.2 LM Studio-managed deployment restores native OpenClaw before v0.9.3
# replaces files.  v0.9.3 itself then manages Ollama only.
existing_mode=$(read_existing_mode)
case "$existing_mode" in
  "") ;;
  passthrough) echo "Existing CogentNexus-OpenClaw already PASSTHROUGH; pre-install native handoff not required." ;;
  managed|maintenance)
    if [ ! -x "$EXISTING_LAUNCHER" ]; then
      echo "Existing CogentNexus-OpenClaw is $existing_mode but launcher is missing: $EXISTING_LAUNCHER. Refusing install mutation before native handoff." >&2
      exit 1
    fi
    echo "Existing CogentNexus-OpenClaw is $existing_mode; entering PASSTHROUGH/native boundary before upgrade mutation."
    "$EXISTING_LAUNCHER" disable
    after_mode=$(read_existing_mode)
    [ "$after_mode" = "passthrough" ] || { echo "Existing CogentNexus-OpenClaw did not reach PASSTHROUGH after disable (mode=$after_mode)." >&2; exit 1; }
    echo "Pre-install native handoff: PASS"
    ;;
  *) echo "Existing CogentNexus-OpenClaw mode '$existing_mode' is not a recognized safe upgrade source." >&2; exit 1 ;;
esac

if [ -n "$MIGRATION_SOURCE" ]; then
  MIGRATION_BACKUP="${XDG_DATA_HOME:-$HOME/.local/share}/CogentNexus-OpenClaw/migration-backups/v$VERSION-$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$MIGRATION_BACKUP"
  for legacy_path in "$WORKSPACE/.cogent" "$WORKSPACE/skills/cogentnexus" "$WORKSPACE/cnx"; do
    [ ! -e "$legacy_path" ] || cp -R "$legacy_path" "$MIGRATION_BACKUP/"
  done
  echo "Backed up proven legacy installation to $MIGRATION_BACKUP"
  MIGRATION_COMPLETE=0
  migration_exit_report() {
    [ "$MIGRATION_COMPLETE" -eq 1 ] && return 0
    [ ! -x "$WORKSPACE/cnxclaw" ] || "$WORKSPACE/cnxclaw" disable >/dev/null 2>&1 || true
    printf '{"status":"INTERRUPTED","productId":"cogentnexus-openclaw","safetyState":"PASSTHROUGH_REQUESTED","backup":"%s","humanDecisionRequired":true}\n' "$MIGRATION_BACKUP" > "$MIGRATION_BACKUP/migration-report.json"
    printf 'CogentNexus-OpenClaw migration interrupted; recoverable report: %s\n' "$MIGRATION_BACKUP/migration-report.json" >&2
  }
  trap migration_exit_report EXIT HUP INT TERM
fi

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
echo "Installed CogentNexus-OpenClaw skill to $TARGET_SKILL"

python "$TARGET_SKILL/scripts/validate.py"
python "$HOST_SCRIPT" --root "$COGENT_ROOT" init

if [ "$SKIP_GATEWAY_RESTART" -eq 1 ]; then
  mode=$(read_existing_mode)
  [ "$mode" = "passthrough" ] || { echo "--skip-gateway-restart staging requires PASSTHROUGH mode." >&2; exit 1; }
fi

if [ "$SKIP_AGENTS_POLICY" -eq 0 ]; then
  python "$HOST_SCRIPT" --root "$COGENT_ROOT" policy apply
fi

if [ "$SKIP_PLUGIN" -eq 0 ]; then
  PLUGIN_DIR="$REPO_ROOT/plugins/cogentnexus-openclaw"
  (
    cd "$PLUGIN_DIR"
    npm ci
    npm run plugin:validate
    node ./scripts/bootstrap-ticket-db.mjs --workspace "$WORKSPACE"
    if [ "$LINK_PLUGIN" -eq 1 ]; then
      openclaw plugins install --link . --force
    else
      PACKAGE_JSON=$(npm pack --json)
      PACKAGE_FILE=$(printf '%s' "$PACKAGE_JSON" | python -c 'import json,sys; x=json.load(sys.stdin); assert isinstance(x,list) and len(x)==1 and x[0].get("filename"); print(x[0]["filename"])')
      trap 'rm -f "$PLUGIN_DIR/$PACKAGE_FILE"' EXIT HUP INT TERM
      openclaw plugins install "npm-pack:$PLUGIN_DIR/$PACKAGE_FILE" --force
      rm -f "$PLUGIN_DIR/$PACKAGE_FILE"
      trap - EXIT HUP INT TERM
    fi
    openclaw plugins disable cogentnexus-openclaw
  )
fi

LAUNCHER="$WORKSPACE/cnxclaw"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env sh
exec python "$CLI_SCRIPT" --root "$COGENT_ROOT" "\$@"
EOF
chmod +x "$LAUNCHER"
echo "Installed CogentNexus-OpenClaw launcher to $LAUNCHER"

set -- "$TARGET_SKILL/scripts/namespace_ownership.py" create --root "$COGENT_ROOT" --workspace "$WORKSPACE" --skill "$TARGET_SKILL" --plugin-path "$(dirname "$WORKSPACE")/extensions/cogentnexus-openclaw" --launcher "$LAUNCHER" --version "$VERSION"
if [ -n "$MIGRATION_SOURCE" ]; then set -- "$@" --migration-source "$MIGRATION_SOURCE"; fi
python "$@" >/dev/null

if [ "$SKIP_GATEWAY_RESTART" -eq 0 ]; then
  python "$CLI_SCRIPT" --root "$COGENT_ROOT" enable --provider ollama
else
  echo "Skipped Host enable because --skip-gateway-restart was requested."
  echo "CogentNexus-OpenClaw remains PASSTHROUGH; run '$LAUNCHER enable' when ready."
fi

openclaw gateway status
python "$TARGET_SKILL/scripts/runtime.py" supervisor doctor
python "$CLI_SCRIPT" --root "$COGENT_ROOT" status

if [ -n "$MIGRATION_SOURCE" ]; then
  openclaw plugins uninstall cogentnexus-rotation --force >/dev/null 2>&1 || true
  rm -rf "$WORKSPACE/.cogent" "$WORKSPACE/skills/cogentnexus" "$WORKSPACE/cnx"
  MIGRATION_COMPLETE=1
  trap - EXIT HUP INT TERM
fi

echo "CogentNexus-OpenClaw v$VERSION installation completed successfully (Ollama-only)."
