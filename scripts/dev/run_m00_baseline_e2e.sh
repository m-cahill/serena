#!/usr/bin/env bash
# M00 Baseline E2E Verification Script (Bash)
# Wraps existing repo commands exactly — no new behavior.
# Usage: ./scripts/dev/run_m00_baseline_e2e.sh
# Prerequisites: Python 3.10.x, Node 18, pip install wait-for-it -r requirements-test.txt

set -e
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

echo "=== M00 Baseline Verification ==="
echo ""

# 1. Python lint (matches CI: ruff 0.3.3)
echo "[1/4] Python lint (ruff)..."
pip install ruff==0.3.3 -q 2>/dev/null || true
ruff .
echo "  PASS"
echo ""

# 2. JS lint (matches CI: npm i --ci, npm run lint)
echo "[2/4] JS lint (eslint)..."
npm i --ci
npm run lint
echo "  PASS"
echo ""

# 3. Env setup (optional — uncomment if running full tests)
# echo "[3/4] Env setup..."
# export TORCH_INDEX_URL=https://download.pytorch.org/whl/cpu
# python launch.py --skip-torch-cuda-test --exit
# echo ""

# 4. Tests require server — print instructions
echo "[3/4] Test server + pytest (manual):"
echo "  Start server in background:"
echo "    python -m coverage run --data-file=.coverage.server launch.py --skip-prepare-environment --skip-torch-cuda-test --test-server --do-not-download-clip --no-half --disable-opt-split-attention --use-cpu all --api-server-stop &"
echo "  Then: wait-for-it --service 127.0.0.1:7860 -t 20"
echo "  Then: python -m pytest -vv --cov . --cov-report=xml --verify-base-url test"
echo ""

echo "=== Lint verification complete ==="
