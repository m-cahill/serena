"""
Gradio 6.10 + Python 3.10 (CI): strip `js=` / `_js=` from event triggers before dispatch.
Some builds raise TypeError on EventListenerMethod when client JS is passed; this keeps UI/API
construction working without changing each call site.

Import this module before `import gradio` (see `initialize.imports`).
"""
from __future__ import annotations

import functools

import gradio.events as ge

_el_setup_ref = getattr(ge.EventListener, "_setup", None)
if _el_setup_ref is None:
    raise RuntimeError("gradio_event_compat: EventListener._setup missing — Gradio API changed")
_orig_el_setup_fn = _el_setup_ref.__func__ if isinstance(_el_setup_ref, staticmethod) else _el_setup_ref


def _event_listener_setup_strip_js(*args, **kwargs):
    raw_trigger = _orig_el_setup_fn(*args, **kwargs)

    @functools.wraps(raw_trigger)
    def event_trigger(block, fn="decorator", **kwargs_inner):
        kwargs_inner.pop("js", None)
        kwargs_inner.pop("_js", None)
        return raw_trigger(block, fn=fn, **kwargs_inner)

    for meta in ("event_name", "has_trigger", "callback", "connection", "event_specific_args"):
        if hasattr(raw_trigger, meta):
            setattr(event_trigger, meta, getattr(raw_trigger, meta))
    return event_trigger


ge.EventListener._setup = (
    staticmethod(_event_listener_setup_strip_js)
    if isinstance(_el_setup_ref, staticmethod)
    else _event_listener_setup_strip_js
)
