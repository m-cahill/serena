# Serena White Paper — Submission Readiness Checklist

**Scope:** `docs/whitepaper/serena_whitepaper_draft.md` (primary), with optional sync to `serena_whitepaper_outline.md` after edits.  
**Constraint:** Edit passes should **preserve** §8 non-claims, **M00–M33** as the core case-study arc, and **M41 / 4.8** only as *subsequent work* (as in §Executive Summary, §7, §4.6, §6.4, §10).

**Draft v2 (2026-05-09):** Publication draft tightened per this checklist; see `serena_whitepaper_v2_edit_report.md` for metrics and verification notes.

| Issue | Severity | Recommended change | File / section | Risk of changing | Required before publication? |
|--------|----------|---------------------|----------------|------------------|---------------------------|
| **Terminology consistency** | Low | Final editorial pass: consistent use of **runtime seam**, **governance loop**, **release-ready**, **allowed legacy surfaces**, **non-claim**, **governed fork** (and **AI-augmented** vs autonomy). Grep the draft before external PDF/export. | Whole draft | Low | **Recommended** (pre-export) |
| **Figure numbering and captions** | Low | Diagrams labeled **Figure 1**, **Figure 2**; each caption states **schematic, not a full call graph** (and cites lock where needed). Add Figure 3+ if more diagrams are introduced later. | §4.1 (current figures) | Low | **Recommended** when figures present |
| **Cross-reference validation** | Medium | After any § merge or appendix move: scan **`§`**, **Appendix**, **see above/below** for orphans; confirm Executive Summary pointers (§7, §8, §3.5, provenance appendix). | Whole draft | Medium if skipped | **Recommended** before submit |
| **High information density; long sentences in Abstract and Introduction** | Medium | Target **15–25%** reduction: shorten compound sentences; trim repeated “governance loop” phrasing after consolidation; compress §5 phase blocks; keep §8 diff-aware. | **§Abstract**, **§1**, **§5** | **Medium** — accidental caveat drop | **Recommended** for external readers |
| **Provenance sits in the Executive Summary front matter** | Low | Move detailed provenance to **Appendix — Provenance and archival hashes**; **one** pointer sentence in Executive Summary. | **§Executive Summary**; appendix | **Low** | **✓ Done (v2)** |
| **Audit rubric not self-contained** | Medium | Short subsection: scale **0–5**, bands, weighted overall, parity baseline vs M33 [Source: `docs/serenav1audit.md` §0]. | **§2.1** (or before §7) | **Low** | **✓ Done (v2)** — §2.1 |
| **“Release-ready” easy to misread** | High (credibility) | **Definition box**: means / does not mean; cross-ref **§8**. | **§1** (+ §8) | **Medium** | **✓ Done (v2)** — blockquote in §1 |
| **Only “after” architecture diagram in body** | Medium | **Before/after** schematic figures with captions. | **§4.1** | **Low** | **✓ Done (v2)** — Figure 1 & 2 |
| **CI tiers described only in prose** | Low | Compact table: tier, marker, workflow(s), purpose, gate; **known asymmetry** (Quality vs Smoke/Linter). | **§6.1** | **Low** — staleness if workflows rename | **✓ Done (v2)** |
| **§3.5 and §3.6 repeat AI cautions** | Low | **Merge** into one **§3.5**; renumber former **§3.7** → **§3.6**; fix cross-refs. | **§3** | **Medium** if refs missed | **✓ Done (v2)** |
| **Non-claims must survive any trim** | High | After reduction, **diff §8**; checklist against `serena_whitepaper_claims_register.md` **non-claim** rows. | **§8**; claims register | **High** if over-edited | **Required** when quoting scores |
| **Core arc M00–M33 vs subsequent M34+** | High | Do not fold Phase VIII–IX into “transformation complete” as the main thesis. Keep **§4.6**, **§7**, **§10** secondary. | **§4.6, §5, §7, §10** | **High** if blurred | **Required** |
| **M41 / 4.8 framing** | Medium | **4.5/5 @ M33** as endpoint; **4.8/5** only as subsequent audit / Phase IX. | **§Abstract**, **§Executive Summary**, **§7**, **§10** | **Medium** | **Required** |
| **Citation density after trimming** | Low | Keep at least one `[Source: …]` per substantive paragraph in **§2, §7, §8** where applicable. | Whole draft | **Low** | **Recommended** |
| **Outline sync** | Low | Match `serena_whitepaper_outline.md` to draft § numbers. | `serena_whitepaper_outline.md` | **Low** | **✓ Done (v2)** |
| **Research notes “partial review” disclaimer** | Low | Optional sentence in appendix on path-level citations vs line-level audit. | `serena_whitepaper_research.md` / draft appendix | **Low** | **Optional** |

---

## Suggested sequencing (when you implement)

0. **Pre-edit hygiene:** Terminology pass, figure caption plan, cross-ref scan — see first three checklist rows. **[Ongoing: run before PDF/export]**  
1. **Appendix / additives:** Provenance move, rubric snippet, release-ready box, CI table, before/after figures. **[largely complete in v2]**  
2. **Merge §3.5–§3.6** and fix cross-refs. **[v2]**  
3. **Density reduction** (15–25%) with **§8 diff** last. **[v2 — ~25% word reduction vs pre-v2 draft]**  
4. **Claims register** spot-check (no new claims; non-claims intact). **[v2 — see report]**  

---

## Definition of “ready to submit” (process)

- [x] Word count or reading-time reduced ~15–25% *or* consciously waived for venue.  
- [x] Provenance not buried in Executive Summary (appendix + one-line pointer).  
- [x] Rubric explained in ≤15 lines.  
- [x] “Release-ready means / does not mean” box present.  
- [x] Before/after architecture figures present.  
- [x] CI tier table present.  
- [x] Single merged AI-governance subsection; no duplicate autonomy disclaimers.  
- [x] §8 non-claims present and aligned with claims register (post-edit review).  
- [x] M33 / 4.5 vs M41 / 4.8 framing verified in Abstract, Executive Summary, §7, §10.  
- [ ] Final terminology + cross-ref grep immediately before external publication artifact.

---

*Checklist updated for **draft v2** (2026-05-09).*
