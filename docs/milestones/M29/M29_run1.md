# M29 — Quality run analysis (run1)

**Date (UTC):** 2026-03-25  
**Repository:** `m-cahill/serena`  
**Branch under test:** `main`

## PRs in scope

| PR | Title (short) | Role |
|----|----------------|------|
| **#64** | M29: health & performance verification (runner metrics + CI snapshot) | Core M29 feature merge |
| **#65** | `requests` 2.33.0 — CVE-2026-25645 (pip-audit) | Unblock blocking audit gate |
| **#66–#67** | transformers pin experiments | Superseded by torch upgrade |
| **#68** | torch **2.2.2+cpu** / torchvision **0.17.2+cpu** | Align PyTorch with `transformers` 4.57 + `register_pytree_node` |
| **#69** | scikit-image **0.25.x** | NumPy 2 ABI (`dtype size changed`) |
| **#70** | `ui.py` — Gradio 6 without `gr.deprecation` | Server import |
| **#71** | `gradio_extensons` — Button `tooltip` shim | Gradio 6 Button kwargs |

**M29 squash merge commit (PR #64):** `f18b73f2` (on `main` history before follow-up fixes).

**Current `main` HEAD (at closeout doc authoring):** `cd56d7c6077e87e987477761c4e399d9b7564d80` (includes #71).

## Binding Quality run

**No passing “binding” Quality run on `main` was achieved during this closeout window.**

The most informative failing run after the dependency and shim chain:

| Field | Value |
|--------|--------|
| **Workflow** | Quality Tests |
| **Run ID** | `23569206049` |
| **URL** | `https://github.com/m-cahill/serena/actions/runs/23569206049` |
| **Outcome** | **failure** |
| **pip-audit** | **passed** (requests CVE + torch/transformers stack consistent) |
| **pytest / server** | **failed** — server startup proceeds further than earlier runs; failure during UI wiring |

### Failure excerpt (root cause)

After `pip-audit`, smoke, and server start, execution fails with **Gradio 6** API drift vs legacy WebUI patterns, for example:

```text
TypeError: EventListener._setup.<locals>.event_trigger() got an unexpected keyword argument '_js'
```

(see `modules/ui_toprow.py` — `.click(..., _js=...)`).

**Gradio 5.x** cannot be selected without violating the **Pillow ≥12** constraint (Gradio 5 requires `pillow<12`; resolver reports unsatisfiable with `pillow>=12`).

### Coverage % and test count

**Not available** from the failing run (pytest step did not complete successfully). Last known fully green reference on this repo remains **M27** Quality run **23513449859** (ledger); **not** claimed as M29 binding.

### Performance artifact

`performance_snapshot.txt` is generated **after** pytest in the workflow. Because pytest did not complete, the **performance-snapshot** artifact was **not** produced for run `23569206049` (workflow annotations: no file at expected path).

---

## Result

**Result:** **BLOCKED** — M29 instrumentation and docs merged; **Quality CI not green** on `main` at closeout time. **Root cause:** **Gradio 6** interaction with existing UI (`_js` on `.click()`, and related 5→6 API differences) **combined with** **Pillow ≥12** (cannot pin Gradio 5 without relaxing Pillow).

**Follow-up (recommended):** dedicated milestone for **Gradio 6 UI event / JS hook migration** (or approved architectural alternative), then re-run binding Quality and attach `performance_snapshot.txt`.

---

## M29.1 — Gradio 6 event kwargs (`_js` → `js`)

**Milestone docs:** `docs/milestones/M29.1/` (plan + toolcalls log).

**Code fix:** Gradio 6 event triggers accept **`js=`** instead of **`_js=`**. Affected `modules/` call sites were updated mechanically (same callback and JS strings; keyword rename only). This addresses the failure in run `23569206049` (`unexpected keyword argument '_js'`).

**Binding Quality run (post–M29.1 code):** merged via **#73** (`m29.1-gradio6-compat`). Subsequent **CI / Gradio** follow-ups: **#74–#78** (torch 2.4+cpu stack, tooltip shims, `Box` alias, `get_config` varargs, `Image` `source`/`tool` compat). Best attempt after **#78**:

| Field | Value |
|--------|--------|
| **Workflow** | Quality Tests |
| **Run ID** | `23573723272` |
| **URL** | `https://github.com/m-cahill/serena/actions/runs/23573723272` |
| **Outcome** | **failure** (pytest exit code 1) |
| **Tests** | **190 passed**, **9 failed** |
| **Coverage (TOTAL)** | **47%** (meets numeric ≥42% gate; pytest still failed overall) |
| **Server** | **starts** (7860 reachable) |
| **`performance_snapshot.txt`** | **Not** produced — workflow skips the write step when pytest fails |

**Example failures:** `test_img2img` → HTTP **422**; `sdapi/v1/cmd-flags`, `samplers`, `progress` → **500**; pydantic **`sampler_index`** validation; **`runtime_metrics`** contract test.

**Binding verdict:** **not PASS** — ledger / audit **stay at 4.0 / 5 pending binding CI** until a **fully green** Quality run **and** confirmed **`performance_snapshot.txt`** artifact.
