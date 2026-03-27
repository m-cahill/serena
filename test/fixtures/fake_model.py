"""M20: Minimal fake model + provider for runner / process_images_inner tests.

M35: Supported-path orchestration uses ``ModelProvider.get_model``; keep
``modules.shared.sd_model`` aligned with the provider return when tests exercise
code that still reads the compatibility ``p.sd_model`` property.
"""

from __future__ import annotations

from contextlib import contextmanager
from types import SimpleNamespace

from modules.runtime.model_provider import ModelProvider


class _DummyDiffusion:
    def to(self, *args, **kwargs):
        return self


class _WrappedModel:
    """`model` sub-object: conditioning_key + diffusion stub for sd_unet."""

    conditioning_key = "crossattn"

    def __init__(self) -> None:
        self.diffusion_model = _DummyDiffusion()


class FakeModel:
    """Minimum surface for M16–M19 runtime + shared.sd_model metadata."""

    latent_channels = 4
    lowvram = False
    is_sdxl = False
    is_sdxl_inpaint = False
    is_sd3 = False
    sd_model_hash = "fake"
    dtype = None
    device = None

    def __init__(self) -> None:
        self.sd_checkpoint_info = SimpleNamespace(
            name_for_extra="fake-checkpoint",
            model_name="fake-checkpoint",
        )
        self.model = _WrappedModel()

    @contextmanager
    def ema_scope(self, *args, **kwargs):
        yield


class FakeModelProvider(ModelProvider):
    """Fixed FakeModel; optional `get_model` call recording."""

    def __init__(
        self,
        model: FakeModel | None = None,
        *,
        track_calls: bool = False,
    ) -> None:
        self._model = model if model is not None else FakeModel()
        self.track_calls = track_calls
        self.get_model_calls: list[object] = []

    def get_model(self, p):
        if self.track_calls:
            self.get_model_calls.append(p)
        return self._model
