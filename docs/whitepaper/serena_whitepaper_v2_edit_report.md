# Serena White Paper — Draft v2 Edit Report

**Date:** 2026-05-09  
**Controlling document:** `docs/whitepaper/serena_submission_readiness_checklist.md`

## Word count

| Version | Approx. words (whitespace-separated) | Change vs v1 baseline |
|--------|--------------------------------------|-------------------------|
| Pre-v2 draft (saved revision) | 5157 | — |
| **Draft v2** | **3866** | **~25.0% reduction** |

*Method:* `len(open(...).read().split())` on `serena_whitepaper_draft.md` (UTF-8).

## Files changed

| Path | Change |
|------|--------|
| `docs/whitepaper/serena_whitepaper_draft.md` | Publication draft v2: provenance appendix, §2.1 rubric, release-ready box, Figure 1/2, CI table, merged §3.5, renumbered §3.6, tightened Abstract/Intro/Method/§5/§6. |
| `docs/whitepaper/serena_whitepaper_outline.md` | Synced to new §3 structure, ES provenance pointer, §2.1, figures, §6.1 table, third appendix. |
| `docs/whitepaper/serena_submission_readiness_checklist.md` | Added three pre-edit rows (terminology, figures, cross-refs); marked v2 completions; updated sequencing and “ready to submit” checkboxes. |
| `docs/whitepaper/serena_whitepaper_v2_edit_report.md` | This report. |

**Not edited:** `docs/serena.md` (per charter).

## Checklist mapping (required items)

- **M00–M33 arc / M33 = 4.5:** Preserved; Abstract, ES, §7 table, §10 unchanged in scoring thesis.
- **M41 / 4.8 subsequent only:** Preserved in Abstract, ES, §4.6, §6.4, §7, §10.
- **Non-claims:** §8 list retained (wording trimmed for density; same substantive items as claims register **non-claim** rows). Autonomy **non-claim** consolidated once in **§3.5**.
- **Provenance:** Full M00 + M33 hash discussion moved to **Appendix — Provenance and archival hashes**; ES has single pointer sentence.

## Checks run

- Manual grep: no stale **§3.7** or **see above** in draft; internal **§3** refs only to architecture lock / **§3.5**.
- **Cross-reference spot-check:** Executive Summary → §3.5, §7, §8, provenance appendix; §7 → §2.1; release-ready box → §8.
- **Workflow names** in CI table match `.github/workflows/`: `run_smoke_tests.yaml`, `run_quality_tests.yaml`, `run_nightly_tests.yaml`, `on_pull_request.yaml`.

## Unresolved / follow-up risks

1. **Exact word-count parity** depends on tokenizer; ~25% is approximate; venue may count differently.
2. **CI table** can drift if workflow files are renamed—pin to `ci_environment_contract.md` in maintenance passes.
3. **Figure / tier prose** should be re-grepped before export (checklist row: terminology + cross-refs).
4. **`docs/milestones/` gitignore** caveat preserved in §6.5; granular run-ID reproduction still workspace-dependent.

---

*End of report.*
