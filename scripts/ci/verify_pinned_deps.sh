#!/usr/bin/env bash
# Verify that pinned packages in a lock/manifest match the active environment.
# - For `pkg==version` lines: exact match via `pip show`.
# - For PEP 508 direct refs (`name @ url`): require package import name installed.
# - Emits pip freeze to dependency_snapshot.txt (or path from 2nd arg).
# M04: originally requirements_versions.txt only.
# M26: requirements-ci.txt + snapshot artifact for reproducibility evidence.
set -euo pipefail

REQUIREMENTS="${1:-requirements-ci.txt}"
SNAPSHOT_OUT="${2:-dependency_snapshot.txt}"

if [[ ! -f "$REQUIREMENTS" ]]; then
  echo "::error::Requirements file not found: $REQUIREMENTS"
  exit 1
fi

pip freeze >"$SNAPSHOT_OUT"
echo "Wrote dependency snapshot to $SNAPSHOT_OUT"

errors=0
while IFS= read -r raw || [[ -n "$raw" ]]; do
  line="${raw#"${raw%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"

  [[ -z "$line" ]] && continue
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  [[ "$line" =~ ^--index-url ]] && continue
  [[ "$line" =~ ^--extra-index-url ]] && continue
  [[ "$line" =~ ^--find-links ]] && continue
  [[ "$line" =~ ^--no-index ]] && continue

  if [[ "$line" =~ ^https?:// ]]; then
    continue
  fi

  if [[ "$line" =~ ^([a-zA-Z0-9][a-zA-Z0-9_.-]*)[[:space:]]+@ ]]; then
    pkg="${BASH_REMATCH[1]}"
    pkg="${pkg//[[:space:]]/}"
    if ! pip show "$pkg" >/dev/null 2>&1; then
      echo "::error::Package not installed (direct reference): $pkg"
      ((errors++)) || true
    fi
    continue
  fi

  [[ "$line" != *"=="* ]] && continue

  pkg="${line%%==*}"
  rest="${line#*==}"
  expected="${rest%%[#]*}"
  pkg="${pkg//[[:space:]]/}"
  expected="${expected//[[:space:]]/}"

  [[ -z "$pkg" || -z "$expected" ]] && continue

  installed=""
  if installed=$(pip show "$pkg" 2>/dev/null | grep -E '^Version:' | awk '{print $2}'); then
    installed="${installed//[[:space:]]/}"
    if [[ "$installed" != "$expected" ]]; then
      echo "::error::Dependency mismatch: $pkg expected $expected got $installed"
      ((errors++)) || true
    fi
  else
    echo "::error::Package not installed: $pkg (expected $expected)"
    ((errors++)) || true
  fi
done <"$REQUIREMENTS"

if [[ $errors -gt 0 ]]; then
  echo "::error::$errors dependency mismatch(es) found"
  exit 1
fi
echo "All pinned dependencies match installed versions."
