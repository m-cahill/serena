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


for _ev_name, _ev in vars(ge.Events).items():
    if isinstance(_ev, ge.EventListener):
        _ev.listener = _wrap_listener(_ev.listener)
