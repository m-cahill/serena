#!/usr/bin/env bash
# M04: Verify that every pinned package in requirements_versions.txt matches installed version.
# Skips unversioned packages (e.g. torch). Fails CI on mismatch.
set -euo pipefail

REQUIREMENTS="${1:-requirements_versions.txt}"

if [[ ! -f "$REQUIREMENTS" ]]; then
  echo "::error::Requirements file not found: $REQUIREMENTS"
  exit 1
fi

errors=0
while IFS= read -r line || [[ -n "$line" ]]; do
  # Skip blank lines and comments
  [[ -z "${line// }" ]] && continue
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  # Skip lines without == (unversioned)
  [[ "$line" != *"=="* ]] && continue

  # Extract package and version (strip inline comments)
  pkg="${line%%==*}"
  rest="${line#*==}"
  expected="${rest%%[# ]*}"
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
done < "$REQUIREMENTS"

if [[ $errors -gt 0 ]]; then
  echo "::error::$errors dependency mismatch(es) found"
  exit 1
fi
echo "All pinned dependencies match installed versions."
