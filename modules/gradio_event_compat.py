"""
Gradio 6.10 + Python 3.10 (CI): strip `js=` / `_js=` from all built-in event listeners.

Some CI builds raise TypeError when client JS is passed into the event path. Wrapping each
`gradio.events.Events.*.listener` before component classes are defined avoids per-call-site edits.

Import this module before `import gradio` (see `initialize.imports`).
"""
from __future__ import annotations

import functools

import gradio.events as ge


def _wrap_listener(raw):
    @functools.wraps(raw)
    def wrapped(block, fn="decorator", **kwargs):
        kwargs.pop("js", None)
        kwargs.pop("_js", None)
        return raw(block, fn=fn, **kwargs)

    for meta in ("event_name", "has_trigger", "callback", "connection", "event_specific_args"):
        if hasattr(raw, meta):
            setattr(wrapped, meta, getattr(raw, meta))
    return wrapped


_EL = getattr(ge, "EventListener", None)
if _EL is not None:
    _to_patch: list = []
    _all = getattr(ge, "all_events", None)
    if _all:
        _to_patch = [e for e in _all if isinstance(e, _EL)]
    else:
        _evs = getattr(ge, "Events", None)
        if _evs is not None:
            _to_patch = [v for v in vars(_evs).values() if isinstance(v, _EL)]
    for _ev in _to_patch:
        _ev.listener = _wrap_listener(_ev.listener)
