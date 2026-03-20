# M19 Plan — Model provider interface

**Milestone:** M19 — Model provider interface  
**Phase:** Phase IV — Runtime Extraction  
**Status:** In progress (canonical plan; execution on branch `m19-model-provider`)

---

## 1. Intent / target

Introduce a **Model Provider** that decouples runtime execution from direct `shared.sd_model` / `p.sd_model` access. Replace implicit globals with an explicit dependency:

```text
runtime → model_provider → model
```

**Not in scope:** Removing `shared.sd_model`, refactoring `sd_models`, extension/API changes, sampler/decode logic changes, performance work.

---

## 2. Invariants

- Public behavior, API, UI, extensions unchanged.
- `process_images()`, `ProcessingRunner` lifecycle and hook order unchanged.
- Same model object, dtype/device, checkpoint/reload semantics as before.
- `RuntimeContext` unchanged in M19.

---

## 3. Design

| Piece | Role |
|--------|------|
| `ModelProvider` | `get_model(self, p)` |
| `SharedModelProvider` | Thin adapter: `import modules.shared as shared` inside `get_model`; return `shared.sd_model` |
| `ProcessingRunner` | `model_provider=` ctor (default `SharedModelProvider()`); `prepare()` sets `request.processing.model_provider` |

Runtime modules (`processing_runtime`, `sampler_runtime`, `decode_runtime`) use **only** `p.model_provider.get_model(p)` for model access. No `p.sd_model` or `shared.sd_model` in those modules (except docstrings / `SharedModelProvider`).

---

## 4. Locked decisions (execution)

1. **Sampler:** Always `model = model_provider.get_model(p)` before `create_sampler`, even when redundant with `p.sd_model` today.  
2. **Injection:** Via `ProcessingRunner`, not `RuntimeContext`.  
3. **Other `shared.*` in decode_runtime:** Only model paths switch to provider; `shared.state`, `shared.opts` unchanged.  
4. **No fallback** `get_model(p) or p.sd_model`.  
5. **Git:** Branch `m19-model-provider`, PR → `main`, merge only with permission.

---

## 5. Deliverables

- [x] `modules/runtime/model_provider.py`
- [x] Runner + runtime wiring
- [x] `test/quality/test_model_provider.py`
- [ ] `M19_run1.md`, `M19_summary.md`, `M19_audit.md`, ledger update (closeout)

---

## 6. Verification

CI: linter, smoke, quality, coverage ≥ 40%. Manual: same seed outputs, no model/device drift.

---

## 7. One-line summary

> Introduce a model provider interface and route runtime model access through it, replacing direct `shared.sd_model` / `p.sd_model` usage in runtime modules.
