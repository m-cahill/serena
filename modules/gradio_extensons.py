import gradio as gr
import gradio.blocks as gb

from modules import scripts, ui_tempdir, patches

# Gradio 6+: `Box` removed — alias to `Group` for legacy `with gr.Box(...)` layouts.
if not hasattr(gr, "Box"):
    gr.Box = gr.Group


def add_classes_to_gradio_component(comp):
    """
    this adds gradio-* to the component for css styling (ie gradio-button to gr.Button), as well as some others
    """

    comp.elem_classes = [f"gradio-{comp.get_block_name()}", *(comp.elem_classes or [])]

    if getattr(comp, 'multiselect', False):
        comp.elem_classes.append('multiselect')


def Component_init(self, *args, **kwargs):
    self.webui_tooltip = kwargs.pop('tooltip', None)

    if scripts.scripts_current is not None:
        scripts.scripts_current.before_component(self, **kwargs)

    scripts.script_callbacks.before_component_callback(self, **kwargs)

    res = original_Component_init(self, *args, **kwargs)

    add_classes_to_gradio_component(self)

    scripts.script_callbacks.after_component_callback(self, **kwargs)

    if scripts.scripts_current is not None:
        scripts.scripts_current.after_component(self, **kwargs)

    return res


def Block_get_config(self, *args, **kwargs):
    # Gradio 6+: `get_config` may pass a second arg (e.g. `cls`) — forward verbatim.
    config = original_Block_get_config(self, *args, **kwargs)

    webui_tooltip = getattr(self, 'webui_tooltip', None)
    if webui_tooltip:
        config["webui_tooltip"] = webui_tooltip

    config.pop('example_inputs', None)

    return config


def BlockContext_init(self, *args, **kwargs):
    if scripts.scripts_current is not None:
        scripts.scripts_current.before_component(self, **kwargs)

    scripts.script_callbacks.before_component_callback(self, **kwargs)

    res = original_BlockContext_init(self, *args, **kwargs)

    add_classes_to_gradio_component(self)

    scripts.script_callbacks.after_component_callback(self, **kwargs)

    if scripts.scripts_current is not None:
        scripts.scripts_current.after_component(self, **kwargs)

    return res


def Blocks_get_config_file(self, *args, **kwargs):
    config = original_Blocks_get_config_file(self, *args, **kwargs)

    for comp_config in config["components"]:
        if "example_inputs" in comp_config:
            comp_config["example_inputs"] = {"serialized": []}

    return config


# Gradio 6+: `IOComponent` was renamed to `Component` (see gradio.components).
original_Component_init = patches.patch(__name__, obj=gr.components.Component, field="__init__", replacement=Component_init)
original_Block_get_config = patches.patch(__name__, obj=gr.blocks.Block, field="get_config", replacement=Block_get_config)
original_BlockContext_init = patches.patch(__name__, obj=gr.blocks.BlockContext, field="__init__", replacement=BlockContext_init)
original_Blocks_get_config_file = patches.patch(__name__, obj=gr.blocks.Blocks, field="get_config_file", replacement=Blocks_get_config_file)


ui_tempdir.install_ui_tempdir_override()

# Gradio 6+: Button.__init__ validates kwargs before Component.__init__ runs; `tooltip` is not a
# valid parameter (tooltips are handled via webui_tooltip in Component_init / get_config).
_gradio_button_orig = gr.Button.__init__


def _gradio_button_init(self, *args, **kwargs):
    wt = kwargs.pop("tooltip", None)
    res = _gradio_button_orig(self, *args, **kwargs)
    if wt is not None:
        self.webui_tooltip = wt
    return res


gr.Button.__init__ = _gradio_button_init

# Gradio 6+: Dropdown / Slider validate kwargs before Component.__init__; strip `tooltip` like Button.
_gradio_dropdown_orig = gr.Dropdown.__init__


def _gradio_dropdown_init(self, *args, **kwargs):
    wt = kwargs.pop("tooltip", None)
    res = _gradio_dropdown_orig(self, *args, **kwargs)
    if wt is not None:
        self.webui_tooltip = wt
    return res


gr.Dropdown.__init__ = _gradio_dropdown_init

_gradio_slider_orig = gr.Slider.__init__


def _gradio_slider_init(self, *args, **kwargs):
    wt = kwargs.pop("tooltip", None)
    res = _gradio_slider_orig(self, *args, **kwargs)
    if wt is not None:
        self.webui_tooltip = wt
    return res


gr.Slider.__init__ = _gradio_slider_init

# Scripts / extras: Checkbox, Number (e.g. xyz_grid, postprocessing_upscale) also reject `tooltip=` before Component.
_gradio_checkbox_orig = gr.Checkbox.__init__


def _gradio_checkbox_init(self, *args, **kwargs):
    wt = kwargs.pop("tooltip", None)
    res = _gradio_checkbox_orig(self, *args, **kwargs)
    if wt is not None:
        self.webui_tooltip = wt
    return res


gr.Checkbox.__init__ = _gradio_checkbox_init

_gradio_number_orig = gr.Number.__init__


def _gradio_number_init(self, *args, **kwargs):
    wt = kwargs.pop("tooltip", None)
    res = _gradio_number_orig(self, *args, **kwargs)
    if wt is not None:
        self.webui_tooltip = wt
    return res


gr.Number.__init__ = _gradio_number_init

# Gradio 6+: `Image` uses `sources=` (not `source=`). Sketch/editor kwargs (`tool`, `brush_color`) belong on
# `ImageEditor`; strip them here so legacy `gr.Image(..., tool=...)` calls still construct (upload-only).
# Smoke CI still installs Gradio 3.x (`requirements_versions.txt`); map `sources=` → `source=` there.
_gradio_image_orig = gr.Image.__init__
_IMAGE_LEGACY_KWARGS = frozenset({"tool", "brush_color"})


def _gradio_major() -> int:
    try:
        return int(str(gr.__version__).split(".", 1)[0])
    except (ValueError, IndexError):
        return 6


def _gradio_image_init(self, *args, **kwargs):
    if _gradio_major() < 6:
        if "sources" in kwargs and "source" not in kwargs:
            sources = kwargs.pop("sources")
            if isinstance(sources, (list, tuple)):
                kwargs["source"] = sources[0] if sources else "upload"
            else:
                kwargs["source"] = sources
    else:
        if "source" in kwargs and "sources" not in kwargs:
            kwargs["sources"] = kwargs.pop("source")
        for k in _IMAGE_LEGACY_KWARGS:
            kwargs.pop(k, None)
    return _gradio_image_orig(self, *args, **kwargs)


gr.Image.__init__ = _gradio_image_init


def _normalize_gradio_event_js_kwargs(kwargs: dict) -> None:
    """Smoke (Gradio 3.x) uses `_js=` on events; Quality / locked CI (Gradio 6+) uses `js=`."""
    if _gradio_major() < 6:
        if "js" in kwargs and "_js" not in kwargs:
            kwargs["_js"] = kwargs.pop("js")
    elif "_js" in kwargs and "js" not in kwargs:
        kwargs["js"] = kwargs.pop("_js")


def _install_event_js_compat():
    """Translate `js` ↔ `_js` so one codebase works on legacy smoke and Gradio 6+ Quality."""
    try:
        from gradio.events import EventListenerMethod  # noqa: PLC0415

        _elm_call = EventListenerMethod.__call__

        def _elm_compat(self, *args, **kwargs):
            _normalize_gradio_event_js_kwargs(kwargs)
            return _elm_call(self, *args, **kwargs)

        EventListenerMethod.__call__ = _elm_compat  # type: ignore[method-assign]
    except ImportError:
        pass

    _seen: set[int] = set()

    def _patch_blocks_config(_cls: type):
        if id(_cls) in _seen or not callable(getattr(_cls, "set_event_trigger", None)):
            return
        _seen.add(id(_cls))
        _orig = _cls.set_event_trigger

        def _cfg_compat(self, *args, **kwargs):
            _normalize_gradio_event_js_kwargs(kwargs)
            return _orig(self, *args, **kwargs)

        _cls.set_event_trigger = _cfg_compat  # type: ignore[method-assign]

    _primary = vars(gb).get("BlocksConfig")
    if _primary is not None:
        _patch_blocks_config(_primary)
    try:
        from gradio.blocks import BlocksConfig as _imp_bc  # noqa: PLC0415

        _patch_blocks_config(_imp_bc)
    except ImportError:
        pass
    for _candidate in vars(gb).values():
        if isinstance(_candidate, type) and _candidate.__name__ == "BlocksConfig":
            _patch_blocks_config(_candidate)
    for _candidate in vars(gb).values():
        if (
            isinstance(_candidate, type)
            and _candidate.__module__ == gb.__name__
            and _candidate.__name__.endswith("Config")
            and callable(getattr(_candidate, "set_event_trigger", None))
        ):
            _patch_blocks_config(_candidate)


_install_event_js_compat()
