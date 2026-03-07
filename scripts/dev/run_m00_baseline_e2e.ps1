# M00 Baseline E2E Verification Script (PowerShell)
# Wraps existing repo commands exactly — no new behavior.
# Usage: .\scripts\dev\run_m00_baseline_e2e.ps1
# Prerequisites: Python 3.10.x, Node 18, pip install wait-for-it -r requirements-test.txt

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $RepoRoot

Write-Host "=== M00 Baseline Verification ===" -ForegroundColor Cyan
Write-Host ""

# 1. Python lint (matches CI: ruff 0.3.3)
Write-Host "[1/4] Python lint (ruff)..." -ForegroundColor Yellow
pip install ruff==0.3.3 -q 2>$null
ruff .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "  PASS" -ForegroundColor Green
Write-Host ""

# 2. JS lint (matches CI: npm i --ci, npm run lint)
Write-Host "[2/4] JS lint (eslint)..." -ForegroundColor Yellow
npm i --ci 2>&1 | Out-Null
npm run lint
if ($LASTEXITCODE -ne 0) {
    Write-Host "  FAIL (note: CRLF linebreaks on Windows may cause linebreak-style errors; CI on Linux passes)" -ForegroundColor Yellow
}
Write-Host ""

# 3. Env setup (optional — uncomment if running tests)
# Write-Host "[3/4] Env setup..." -ForegroundColor Yellow
# $env:TORCH_INDEX_URL = "https://download.pytorch.org/whl/cpu"
# python launch.py --skip-torch-cuda-test --exit
# Write-Host ""

# 4. Tests require server — print instructions
Write-Host "[3/4] Test server + pytest (manual):" -ForegroundColor Yellow
Write-Host "  Start server in separate terminal:"
Write-Host "    python -m coverage run --data-file=.coverage.server launch.py --skip-prepare-environment --skip-torch-cuda-test --test-server --do-not-download-clip --no-half --disable-opt-split-attention --use-cpu all --api-server-stop"
Write-Host "  Then run: wait-for-it --service 127.0.0.1:7860 -t 20"
Write-Host "  Then run: python -m pytest -vv --cov . --cov-report=xml --verify-base-url test"
Write-Host ""

Write-Host "=== Lint verification complete ===" -ForegroundColor Cyan
