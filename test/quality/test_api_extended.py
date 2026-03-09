"""Extended API tests for quality tier. Increases coverage of API endpoints."""
import pytest
import requests


@pytest.mark.parametrize("url", [
    "sdapi/v1/progress",
    "sdapi/v1/sd-vae",
    "sdapi/v1/latent-upscale-modes",
    "sdapi/v1/memory",
    "sdapi/v1/scripts",
    "sdapi/v1/script-info",
    "sdapi/v1/extensions",
])
def test_get_api_endpoint(base_url, url):
    """Verify extended API endpoints return 200."""
    assert requests.get(f"{base_url}/{url}").status_code == 200


<<<<<<< HEAD
=======
def test_interrogate_deepbooru(base_url, img2img_basic_image_base64):
    """Interrogate with deepbooru model."""
    payload = {"image": img2img_basic_image_base64, "model": "deepbooru"}
    assert requests.post(f"{base_url}/sdapi/v1/interrogate", json=payload).status_code == 200


>>>>>>> origin/main
def test_png_info(base_url, img2img_basic_image_base64):
    """PNG info endpoint."""
    payload = {"image": img2img_basic_image_base64}
    assert requests.post(f"{base_url}/sdapi/v1/png-info", json=payload).status_code == 200


def test_extra_batch_images(base_url, img2img_basic_image_base64):
    """Extra batch images API."""
    batch_payload = {
        "resize_mode": 0,
        "show_extras_results": True,
        "gfpgan_visibility": 0,
        "codeformer_visibility": 0,
        "codeformer_weight": 0,
        "upscaling_resize": 2,
        "upscaling_resize_w": 128,
        "upscaling_resize_h": 128,
        "upscaling_crop": True,
        "upscaler_1": "Lanczos",
        "upscaler_2": "None",
        "extras_upscaler_2_visibility": 0,
        "imageList": [{"data": img2img_basic_image_base64, "name": "test.png"}],
    }
    assert requests.post(f"{base_url}/sdapi/v1/extra-batch-images", json=batch_payload).status_code == 200
