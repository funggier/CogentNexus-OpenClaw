#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
WORKSPACE=${OPENCLAW_WORKSPACE:-"$HOME/.openclaw/workspace"}
PROVIDER=""
SKIP_PLUGIN=0
SKIP_GATEWAY_RESTART=0
LINK_PLUGIN=0
SKIP_AGENTS_POLICY=0
VERSION=$(cat "$REPO_ROOT/VERSION" 2>/dev/null || printf 'unknown')

usage() { echo "Usage: $0 [--workspace PATH] [--provider ollama|lmstudio] [--skip-plugin] [--skip-gateway-restart] [--skip-agents-policy] [--link-plugin]"; }

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workspace) [ "$#" -ge 2 ] || { usage; exit 2; }; WORKSPACE=$2; shift 2 ;;
    --provider)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      PROVIDER=$2
      case "$PROVIDER" in ollama|lmstudio) ;; *) echo "Unsupported provider: $PROVIDER" >&2; exit 2 ;; esac
      shift 2 ;;
    --skip-plugin) SKIP_PLUGIN=1; shift ;;
    --skip-gateway-restart) SKIP_GATEWAY_RESTART=1; shift ;;
    --skip-agents-policy) SKIP_AGENTS_POLICY=1; shift ;;
    --link-plugin) LINK_PLUGIN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage; exit 2 ;;
  esac
done

echo "Installing CogentNexus v$VERSION"
[ -n "$PROVIDER" ] && echo "Requested provider: $PROVIDER"

if { [ "$SKIP_PLUGIN" -eq 1 ] || [ "$SKIP_AGENTS_POLICY" -eq 1 ]; } && [ "$SKIP_GATEWAY_RESTART" -eq 0 ]; then
  echo "--skip-plugin and --skip-agents-policy are staging-only options. Use them with --skip-gateway-restart." >&2
  exit 2
fi

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
CLI_SCRIPT="$TARGET_SKILL/scripts/cnx.py"
COGENT_ROOT="$WORKSPACE/.cogent"
CONTROLLER_PATH="$COGENT_ROOT/host/controller.json"
EXISTING_LAUNCHER="$WORKSPACE/cnx"

read_existing_mode() {
  [ -f "$CONTROLLER_PATH" ] || { printf '%s' ''; return 0; }
  python - "$CONTROLLER_PATH" <<'PY'
import json,sys
from pathlib import Path
path=Path(sys.argv[1])
try:
    value=json.loads(path.read_text(encoding='utf-8'))
except Exception as error:
    raise SystemExit(f"Existing CogentNexus controller is unreadable; refusing install mutation: {error}")
mode=value.get('mode') if isinstance(value,dict) else None
if not isinstance(mode,str) or not mode.strip():
    raise SystemExit("Existing CogentNexus controller has no mode; refusing install mutation.")
print(mode)
PY
}

# Never replace an installed skill/plugin while the previous Host still owns
# MANAGED authority. The old launcher is deliberately used before any file
# mutation so its own disable path restores and verifies native OpenClaw first.
existing_mode=$(read_existing_mode)
case "$existing_mode" in
  "") ;;
  passthrough)
    echo "Existing CogentNexus already PASSTHROUGH; pre-install native handoff not required."
    ;;
  managed|maintenance)
    if [ ! -x "$EXISTING_LAUNCHER" ]; then
      echo "Existing CogentNexus is $existing_mode but launcher is missing: $EXISTING_LAUNCHER. Refusing install mutation before native handoff." >&2
      exit 1
    fi
    echo "Existing CogentNexus is $existing_mode; entering PASSTHROUGH/native boundary before upgrade mutation."
    "$EXISTING_LAUNCHER" disable
    after_mode=$(read_existing_mode)
    if [ "$after_mode" != "passthrough" ]; then
      echo "Existing CogentNexus did not reach PASSTHROUGH after disable (mode=$after_mode); refusing install mutation." >&2
      exit 1
    fi
    echo "Pre-install native handoff: PASS"
    ;;
  *)
    echo "Existing CogentNexus mode '$existing_mode' is not a recognized safe upgrade source; refusing install mutation." >&2
    exit 1
    ;;
esac

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
python "$HOST_SCRIPT" --root "$COGENT_ROOT" init

if [ "$SKIP_GATEWAY_RESTART" -eq 1 ]; then
  mode=$(python - "$CONTROLLER_PATH" <<'PY'
import json,sys
from pathlib import Path
path=Path(sys.argv[1])
try: print(json.loads(path.read_text(encoding='utf-8')).get('mode',''))
except Exception: print('')
PY
)
  if [ "$mode" != "passthrough" ]; then
    echo "--skip-gateway-restart safe staging requires CogentNexus PASSTHROUGH mode. Run 'cnx disable' before staging an upgrade." >&2
    exit 1
  fi
fi

if [ "$SKIP_AGENTS_POLICY" -eq 0 ]; then
  python "$HOST_SCRIPT" --root "$COGENT_ROOT" policy apply
fi

if [ "$SKIP_PLUGIN" -eq 0 ]; then
  (
    cd "$REPO_ROOT/plugins/cogentnexus-rotation"
    npm ci
    npm run plugin:validate
    node ./scripts/bootstrap-ticket-db.mjs --workspace "$WORKSPACE"
    if [ "$LINK_PLUGIN" -eq 1 ]; then
      openclaw plugins install --link . --force
    else
      if current_paths=$(openclaw config get plugins.load.paths 2>/dev/null); then
        filtered_paths=$(printf '%s' "$current_paths" | python "$REPO_ROOT/scripts/filter_plugin_paths.py" --plugin-id cogentnexus-rotation)
        openclaw config set plugins.load.paths "$filtered_paths" --strict-json --replace
      fi
      openclaw plugins install . --force
    fi
    openclaw plugins disable cogentnexus-rotation
  )
fi

LAUNCHER="$WORKSPACE/cnx"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env sh
exec python "$CLI_SCRIPT" --root "$COGENT_ROOT" "\$@"
EOF
chmod +x "$LAUNCHER"
echo "Installed CogentNexus launcher to $LAUNCHER"

if [ "$SKIP_GATEWAY_RESTART" -eq 0 ]; then
  if [ -n "$PROVIDER" ]; then
    python "$CLI_SCRIPT" --root "$COGENT_ROOT" enable --provider "$PROVIDER"
  else
    python "$CLI_SCRIPT" --root "$COGENT_ROOT" enable || {
      echo "CogentNexus enable failed. If both Ollama and LM Studio are installed, rerun with --provider ollama or --provider lmstudio." >&2
      exit 1
    }
  fi
else
  echo "Skipped Host enable because --skip-gateway-restart was requested."
  echo "CogentNexus remains PASSTHROUGH with its plugin disabled."
  if [ -n "$PROVIDER" ]; then
    echo "Provider was not committed during staging; run '$LAUNCHER enable --provider $PROVIDER' when ready."
  else
    echo "Run '$LAUNCHER enable [--provider ollama|lmstudio]' when ready."
  fi
fi

openclaw gateway status || [ "$SKIP_GATEWAY_RESTART" -eq 1 ]
python "$TARGET_SKILL/scripts/runtime.py" supervisor doctor
python "$CLI_SCRIPT" --root "$COGENT_ROOT" status

echo "CogentNexus v$VERSION installation completed successfully."
echo "Control it with: $LAUNCHER status|check|provider|start|stop|restart|gateway|ticket|session|policy|disable|enable|reset|uninstall"
