# Serena White Paper Outline

**Planning outline — mirrors `serena_whitepaper_draft.md` section order.** Use the draft for canonical numbering and prose; this file is for structure and bullets only.

## Working Title

**Serena: Audit-First AI-Augmented Refactoring of a Monolithic AI WebUI into a Governed Inference Runtime**

## Abstract

(Short summary in draft v2.)

## Executive Summary

- Bullets: baseline **2.4/5**, **M33** endpoint **4.5/5**, method, architecture, governance, primary lesson (→ **§3.5**).
- **One-line provenance pointer** → Appendix — Provenance and archival hashes (details not in ES).

## 1. Introduction

- Coupling, globals, extensions, CI honesty; **governance loop** thesis.
- **Release-ready means / does not mean** callout; **§8** for full non-claims.
- Scope: **M00–M33**; Phase VIII–IX / **M41** as **subsequent work** only.

## 2. Baseline Audit

- Pre-refactor **2.4/5**: categories, weaknesses, strengths, `process_images` funnel.
- CI score as *trust* problem.
- **§2.1 Scoring rubric (0–5)** — bands, weighted overall, comparability baseline vs M33.

## 3. Method

- **§3.1** — Principles and invariants; **§3.2** — Milestone mechanics; **§3.3** — Audit scoring as steering.
- **§3.4** — Documentation hierarchy (ledger, architecture lock, **allowed legacy surfaces**).
- **§3.5** — **AI-augmented governance**: non-claims, numbered loop, evidenced artifacts (single merged subsection).
- **§3.6** — Evidence bundles, doc-only milestones, **release-ready** semantics.

## 4. Architectural Transformation

- **Figure 1** baseline schematic; **Figure 2** governed runtime schematic (§4.1).
- **ProcessingRunner**, extraction, **ModelProvider**, UI/extension contract.
- **§4.6** — Subsequent work only (Phase VIII+).

## 5. Phase-by-Phase Case Study (M00–M33)

- Phases I–VII (compressed narrative in v2).
- **§5.1** — Cross-cutting observations.

## 6. Verification and Governance

- **§6.1** — CI tier **table** + three-tier narrative; Smoke / Quality / Nightly / Linter; **known asymmetry**.
- **§6.1b** — JavaScript lint reproducibility.
- **§6.2** — pytest-only coverage; **§6.3** — pip-audit deferrals; **§6.4** — M29 vs **M41** subsequent.
- **§6.5** — Docs / gitignore caveat; **§6.6** — Radon.

## 7. Results

- Table **2.4 → 4.5** at M33; tie to **§2.1** rubric.
- **Subsequent work:** **M41 / 4.8** — not core endpoint.

## 8. Limits and Non-Claims

- Image quality, perf, globals, extensions, vulns, semantic equivalence, drop-in, etc.
- **Release-ready** = governance, not enterprise production certification.

## 9. Lessons Learned

- Truth before motion; seams; runner; ModelProvider; mockability; lock; agents; deferrals; doc milestones.

## 10. Conclusion

- **Governed fork** pattern; three filters; **M41** as continuity only.

## Appendices (draft v2)

- **Evidence reference key** (S1–S5).
- **Research and claim hygiene** (research doc, claims register).
- **Provenance and archival hashes** (M00 date note; M33 SHA vs tag).

---

*End of outline.*
