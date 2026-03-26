"""
Gradio 6.10 + Python 3.10 (CI): strip `js=` / `_js=` from event listener callables.

`ComponentMeta` uses `EventListener.copy()` and `EventListener(...)` for each component;
wrapping only `Events.*` is insufficient because `.copy()` rebuilds listeners via `__init__`.
Patch `EventListener.__init__` to wrap `self.listener` after the stock `_setup` runs.

Import this module before `import gradio` (see `initialize.imports`).
"""
from __future__ import annotations

import functools

import gradio.events as ge


def _wrap_listener(raw):
    if getattr(raw, "_webui_strip_js", False):
        return raw

    @functools.wraps(raw)
    def wrapped(block, fn="decorator", **kwargs):
        kwargs.pop("js", None)
        kwargs.pop("_js", None)
        return raw(block, fn=fn, **kwargs)

    for meta in ("event_name", "has_trigger", "callback", "connection", "event_specific_args"):
        if hasattr(raw, meta):
            setattr(wrapped, meta, getattr(raw, meta))
    wrapped._webui_strip_js = True  # type: ignore[attr-defined]
    return wrapped


_el = getattr(ge, "EventListener", None)
if _el is not None:
    _orig_init = _el.__init__

    def _init_strip_js(self, *args, **kwargs):
        _orig_init(self, *args, **kwargs)
        # Gradio 6+: Component.__init__ may call EventListener.__init__(self) cooperatively;
        # only real EventListener (str subclass) instances define `listener`.
        if isinstance(self, _el) and hasattr(self, "listener"):
            self.listener = _wrap_listener(self.listener)

    _el.__init__ = _init_strip_js  # type: ignore[method-assign]
