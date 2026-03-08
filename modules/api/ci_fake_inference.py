"""
CI-only fake inference for txt2img and img2img API endpoints.

When CI=true (e.g. GitHub Actions), these endpoints return a deterministic
1×1 PNG instead of invoking the model pipeline. This allows API contract
tests to pass without requiring real model inference.
"""

from modules.api import models

# 1x1 transparent PNG (base64)
_FAKE_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCA"
    "O5vX8cAAAAASUVORK5CYII="
)


def ci_fake_txt2img():
    """Return a deterministic TextToImageResponse for CI."""
    return models.TextToImageResponse(
        images=[_FAKE_PNG],
        parameters={},
        info="ci-fake-image",
    )


def ci_fake_img2img():
    """Return a deterministic ImageToImageResponse for CI."""
    return models.ImageToImageResponse(
        images=[_FAKE_PNG],
        parameters={},
        info="ci-fake-image",
    )
