# Extension API deprecation policy (Serena)

**Scope:** Callback categories registered through `modules/script_callbacks.py` and declared in `modules/extension_api.py` (`SUPPORTED_CALLBACKS`, `EXTENSION_API_VERSION`).

**Related:** `docs/architecture/extension_api_contract_v1.md` (v1.0 contract).

---

## Additive changes in v1.x

- Prefer **adding** categories, optional parameters, or new fields on existing callback parameter objects over breaking changes.
- Any new category must update `SUPPORTED_CALLBACKS`, the contract document, milestone notes, and quality tests that lock the registry.

## Soft deprecation

- Use `modules/deprecation.py` (`warn_deprecated`, `@deprecated`) and `script_callbacks.deprecate_callback` to emit **`DeprecationWarning`** with the fixed prefix `Serena extension API:` so logs and test filters stay consistent.
- Soft deprecation is **opt-in at call sites**: scaffolding does nothing until code explicitly invokes these helpers.
- Milestone documentation must state what is deprecated, what replaces it, and the intended timeline.

## Hard removal

- Removing or renaming a callback category, or intentionally changing invocation order or `ordered_callbacks` behavior, is **breaking** and requires:
  - A new **`EXTENSION_API_VERSION`** (per program governance), and
  - Explicit milestone approval and contract updates.

## Milestone documentation

Each deprecation milestone must record:

- Affected category names (or symbols).
- Replacement API (if any).
- Warning mechanism used (`warn_deprecated`, `deprecate_callback`, or `@deprecated`).
- Whether behavior is shimmed, aliased, or unchanged.

---

## Compatibility shims (pattern)

When renaming is unavoidable before a major bump, keep the old `callback_map` entry and dispatch path, forward to the new registration surface, and emit `deprecate_callback` from the old path until authors migrate. An illustrative comment lives in `script_callbacks.py` under **M25 Deprecation & Compatibility Scaffolding**.
