# M28 — Summary (security & supply-chain hardening)

**Status:** **Complete** (append **Quality run ID** to **`M28_run1.md`** after the first green **Quality** workflow on the release merge).  
**Branch:** `m28-security-supply-chain`  
**Annotated tag:** **`v0.0.28-m28`** → **`c97c4067820210f9c55e8fa56d363ddb21fdb547`** (ledger short-hash commit; finalization docs in parent **`f88e1e9c`**). Verify with **`git show v0.0.28-m28`**.

---

## Objectives achieved

1. **Blocking `pip-audit`** on **Quality** (**M28a**) — merge gate fails on unresolved advisories (was warning-only in M26–M27).
2. **M28b remediation** — small-batch upgrades across HTTP, API, tooling, Pillow/Gradio/NumPy, and ML stack (**protobuf**, **pytorch-lightning**, **transformers**, co-deps).
3. **Governed deferrals** — only **CVE-2025-69872** (**diskcache**) and **CVE-2026-4539** (**pygments**), **no fix on PyPI** at closeout; **`--ignore-vuln`** in workflow + **`ci_environment_contract.md`** + **`M28_run1.md`**.
4. **No CI weakening** — no `continue-on-error` on audit, no lowered coverage floor (**≥42%** unchanged), **`set -o pipefail`** preserved.

---

## Upgrade batches (M28b)

| Batch | Focus | Notes |
|-------|--------|--------|
| 1 | HTTP stack | `requests`, `urllib3`, `certifi`, `idna` |
| 2 | Pillow 10.x path | `blendmodes` co-bump |
| 3 | API stack | `fastapi`, `starlette`, `h11`, `httpx` / `httpcore` |
| 4 | Tooling | `setuptools`, `wheel`, `filelock`, `GitPython` |
| 5a | Pillow **12** + graph | **NumPy 2**, **blendmodes 2025**, **Gradio 6**; minimal UI adapters |
| 5a stabilization | Gradio 6 | `IOComponent` → `Component`, `ui_tempdir` guard |
| 5b step 1 | **protobuf** ≥5 | **`open-clip-torch`** ≥2.24 (dropped `protobuf<4` cap) |
| 5b step 2 | **pytorch-lightning** 2.x | Trainer stack; existing PL2 shim |
| 5b step 3 | **transformers** 4.57.x | **`safetensors`** ≥0.4.3, **Gradio** ≥6.7 (CVEs) |
| Finalization | Deferrals | Workflow **`--ignore-vuln`** for **diskcache** / **pygments** only |

---

## Final CVE state

| Category | State |
|----------|--------|
| **Resolvable via PyPI** | **Cleared** through M28b pins |
| **No PyPI fix** | **2** — **diskcache** (CVE-2025-69872), **pygments** (CVE-2026-4539) |
| **Effective audit** | **0** failing rows with **2** documented ignores (any *new* CVE still **fails** Quality) |
| **torch/torchvision +cpu** | Still **skipped** in `pip-audit -r` mode; installed in CI |

---

## Deferral rationale

- **diskcache:** Latest **5.6.3**; pickle-deserialization class of issue; **follow-up:** bump when upstream releases; avoid untrusted cache dirs.
- **pygments:** Latest **2.19.2**; advisory cites fix **≥2.19.3** — **not published**; **follow-up:** pin **`pygments>=2.19.3`** when available.

---

## System stability

- **Determinism:** **`requirements-ci.txt`** remains uv-compiled from **`requirements-ci.in`**; **CLIP** still pinned in workflow.
- **Behavior:** Dependency-driven changes confined to **compatibility shims** (e.g. Gradio 6, Pydantic v2 API surface) where required; no intentional generation-semantics drift.

---

## References

- **`M28_run1.md`** — evidence, batch metrics, deferral table, **Quality run ID** (append).
- **`M28_audit.md`** — verdict and governance checklist.
- **`docs/architecture/ci_environment_contract.md`** — **pip-audit deferrals (M28)**.
