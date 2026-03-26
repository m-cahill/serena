# Serena — Evidence matrix (by phase)

Compact mapping: **phase** → **milestone range** → **primary gain** → **binding proof** (CI run ID or artifact where applicable). Earlier milestones are summarized from `docs/serena.md`; **M26–M29** were cross-checked for M30.

---

## Phase I — Baseline and guardrails (M00–M04)

| Milestone range | Primary gain | Binding proof |
|-----------------|--------------|---------------|
| M00–M04 | Baseline freeze, CI truthfulness, smoke/quality/nightly tiers, coverage and security guardrails | Ledger: e.g. M04 Quality **22871471473**; see `docs/serena.md` §4 |

---

## Phase II — Runtime seam preparation (M05–M09)

| Milestone range | Primary gain | Binding proof |
|-----------------|--------------|---------------|
| M05–M09 | Temporary opts, prompt/seed prep, opts snapshot, execution context | Ledger: e.g. M09 Quality **22986731960**; see `docs/serena.md` §4 |

---

## Phase III — Runner and service boundary (M10–M15)

| Milestone range | Primary gain | Binding proof |
|-----------------|--------------|---------------|
| M10–M15 | `ProcessingRunner`, lifecycle, hooks, txt2img/API through runner, queue seam | Ledger: e.g. M15 Quality **23232040072**; see `docs/serena.md` §4 |

---

## Phase IV — Runtime extraction (M16–M20)

| Milestone range | Primary gain | Binding proof |
|-----------------|--------------|---------------|
| M16–M20 | `processing_runtime`, `sampler_runtime`, `decode_runtime`, `ModelProvider`, mockable pipeline tests | Ledger: M20 Quality **23333740069** @ **9c7e693a**; tag **v0.0.20-m20** per ledger |

---

## Phase V — UI and extension stabilization (M21–M25)

| Milestone range | Primary gain | Binding proof |
|-----------------|--------------|---------------|
| M21–M25 | Tab registry, modular txt2img/img2img/settings/extensions, extension API v1, deprecation scaffolding | Ledger: M25 Quality **23421440167** @ **46891797** |

---

## Phase VI — Hardening and reproducibility (M26–M29)

| Milestone range | Primary gain | Binding proof |
|-----------------|--------------|---------------|
| **M26** | Locked `requirements-ci.txt`, CLIP install contract, npm `npm ci`, reproducibility artifacts | Quality **23467772232** (112 pass, 40% cov per `M26_run1.md`) |
| **M27** | Coverage floor **≥42%**, pytest-only gate, Radon warn-first | Quality **23513449859** (198 pass, 47% pytest-only) |
| **M28** | Blocking `pip-audit`, M28b upgrades, **two** documented deferrals | No isolated green Quality on **`main`** for M28 alone — **PR #64** squash with M29; first **`main`** Quality **23566817312** failed; stack proof **23618918747** (`M30_run1.md` §3) |
| **M29** | Runner `runtime_metrics`, DEBUG API timing, `performance_snapshot.txt` | Quality **23618918747** (199 pass, ~48% cov, artifact); tag **v0.0.29-m29** @ **1b2e2f69** |

---

## Phase VII — Release lock (M31–M33)

| Milestone range | Primary gain | Binding proof |
|-----------------|--------------|---------------|
| **M31** | Architecture lock (`serena_architecture_lock.md`, `serena_allowed_legacy_surfaces.md`); documentation only | Ledger + lock docs; no runtime gate (same posture as M30 for doc-only) |
| **M32** | Evidence/audit closure (synthesis of ledger + lock + bundle + matrix + milestone runs); documentation only | Ledger + `M32_run1.md`; no new runtime gate; binding technical proof remains at cited milestones (e.g. M29 Quality **23618918747**) |
| **M33** | Release-ready 5/5 close | *Pending* |
