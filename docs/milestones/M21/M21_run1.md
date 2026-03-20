# M21 — CI run 1 (PR #40)

**Branch:** `m21-ui-tab-registry`  
**PR:** https://github.com/m-cahill/serena/pull/40  
**Head (at run capture):** implementation tip `b2a11209`; branch may advance with doc-only commits — see PR for current SHA.

## Required PR checks (green)

| Check | Run / job | Result |
|-------|-----------|--------|
| ruff | [23360537402](https://github.com/m-cahill/serena/actions/runs/23360537402) | pass |
| eslint | same workflow | pass |
| smoke tests | [23360545341](https://github.com/m-cahill/serena/actions/runs/23360545341) | pass (~2m51s) |

Additional eslint/ruff rows appeared on a second workflow run (`23360545351`); all passed.

## Post-merge

- [x] Quality workflow on `main`: [23361011739](https://github.com/m-cahill/serena/actions/runs/23361011739) @ `081de7e7` — **success**, 92 passed, 40% coverage.
- [x] Closeout docs + tag `v0.0.21-m21` on `081de7e7` (after ledger/summary/audit on `main`).
