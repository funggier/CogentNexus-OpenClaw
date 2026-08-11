#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
WORKSPACE=${OPENCLAW_WORKSPACE:-"$HOME/.openclaw/workspace"}
SKIP_PLUGIN=0
SKIP_GATEWAY_RESTART=0
LINK_PLUGIN=0

usage() { echo "Usage: $0 [--workspace PATH] [--skip-plugin] [--skip-gateway-restart] [--link-plugin]"; }

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workspace) [ "$#" -ge 2 ] || { usage; exit 2; }; WORKSPACE=$2; shift 2 ;;
    --skip-plugin) SKIP_PLUGIN=1; shift ;;
    --skip-gateway-restart) SKIP_GATEWAY_RESTART=1; shift ;;
    --link-plugin) LINK_PLUGIN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage; exit 2 ;;
  esac
done

for command_name in python openclaw; do
  command -v "$command_name" >/dev/null 2>&1 || { echo "Required command not found: $command_name" >&2; exit 1; }
done
if [ "$SKIP_PLUGIN" -eq 0 ]; then
  command -v npm >/dev/null 2>&1 || { echo "Required command not found: npm" >&2; exit 1; }
fi
python -c "import yaml" >/dev/null 2>&1 || {
  echo "PyYAML is required. Run: python -m pip install -r requirements-dev.txt" >&2
  exit 1
}

SOURCE_SKILL="$REPO_ROOT/skills/cogentnexus"
TARGET_SKILL="$WORKSPACE/skills/cogentnexus"
STAGED_SKILL="$WORKSPACE/.cogent/install-staging/cogentnexus"
BACKUP_ROOT="$WORKSPACE/.cogent/install-backups"
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

python "$TARGET_SKILL/scripts/validate.py" --workspace-singleton
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
  )
fi
if [ "$SKIP_GATEWAY_RESTART" -eq 0 ]; then openclaw gateway restart; fi
openclaw gateway status
python "$TARGET_SKILL/scripts/phase3.py" supervisor doctor
echo "CogentNexus installation completed successfully."
