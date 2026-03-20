"""M19: Injectable model access for runtime modules.

Runtime must not read shared.sd_model or p.sd_model directly; use
model_provider.get_model(p) instead. Default implementation delegates to shared.
"""

from __future__ import annotations


class ModelProvider:
    """Abstract model source for the generation runtime."""

    def get_model(self, p):
        raise NotImplementedError


class SharedModelProvider(ModelProvider):
    """Default provider: returns the globally loaded model (current webui behavior)."""

    def get_model(self, p):
        import modules.shared as shared

        return shared.sd_model
