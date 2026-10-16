#!/usr/bin/env bash
# Rebuild the generated files and run every check on the lab module. Run from anywhere.
set -euo pipefail
LAB="$(cd "$(dirname "$0")/.." && pwd)"
cd "$LAB"
export PYTHONDONTWRITEBYTECODE=1
TOOLSMITH="$LAB/.agents/skills/bmad-toolsmith/scripts"
status=0

echo "== rebuild agents, roster, manifests and README figures"
uv run --no-cache tools/build_cast.py
uv run --no-cache tools/readme_figures.py

if [ -d "$TOOLSMITH" ]; then
  echo "== skill checks"
  for d in skills/*/; do
    out=$(uv run --no-cache "$TOOLSMITH/init_skill.py" --check "$d" --any-name) || { echo "FAIL init_skill $d"; echo "$out"; status=1; }
    out=$(uv run --no-cache "$TOOLSMITH/scan_paths.py" "$d" || true)
    echo "$out" | python3 -c "import json,sys; f=json.load(sys.stdin).get('findings',[]); sys.exit(1 if f else 0)" || { echo "paths $d: $out"; status=1; }
    if [ -d "$d/scripts" ]; then
      out=$(uv run --no-cache "$TOOLSMITH/scan_scripts.py" "$d" || true)
      # refcheck.py must query Crossref and arXiv; its docstring says why. Every other finding fails.
      echo "$out" | python3 -c "import json,sys; f=[x for x in json.load(sys.stdin).get('findings',[]) if not (x['rule']=='network-call' and x['path'].endswith('refcheck.py'))]; sys.exit(1 if f else 0)" || { echo "scripts $d: $out"; status=1; }
    fi
  done
else
  echo "(toolsmith not installed here; skipping skill checks)"
fi

echo "== manifests"
if [ -f _bmad/scripts/validate_manifests.py ]; then
  uv run --no-cache _bmad/scripts/validate_manifests.py --project-root "$LAB" || status=1
else
  echo "(BMad is not set up in this clone; skipping the manifest check. CONTRIBUTING.md says how to add it.)"
fi

echo "== script tests"
for t in skills/*/scripts/tests; do
  uv run --no-cache --with pytest pytest -q -p no:cacheprovider "$t" || status=1
done

find skills -name "__pycache__" -type d -prune -exec rm -rf {} +
[ "$status" -eq 0 ] && echo "ALL CHECKS PASSED" || echo "CHECKS FAILED"
exit "$status"
