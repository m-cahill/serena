import base64
import os

import pytest

test_files_path = os.path.dirname(__file__) + "/test_files"
test_outputs_path = os.path.dirname(__file__) + "/test_outputs"


def pytest_configure(config):
    # We don't want to fail on Py.test command line arguments being
    # parsed by webui:
    os.environ.setdefault("IGNORE_CMD_ARGS_ERRORS", "1")


def pytest_collection_modifyitems(config, items):
    """Apply smoke/quality/nightly markers based on test path."""
    for item in items:
        path_str = str(item.path)
        if "/smoke/" in path_str or "\\smoke\\" in path_str:
            item.add_marker(pytest.mark.smoke)
        elif "/quality/" in path_str or "\\quality\\" in path_str:
            item.add_marker(pytest.mark.quality)
        elif "/nightly/" in path_str or "\\nightly\\" in path_str:
            item.add_marker(pytest.mark.nightly)


def file_to_base64(filename):
    with open(filename, "rb") as file:
        data = file.read()

    base64_str = str(base64.b64encode(data), "utf-8")
    return "data:image/png;base64," + base64_str


@pytest.fixture(scope="session")  # session so we don't read this over and over
def img2img_basic_image_base64() -> str:
    return file_to_base64(os.path.join(test_files_path, "img2img_basic.png"))


@pytest.fixture(scope="session")  # session so we don't read this over and over
def mask_basic_image_base64() -> str:
    return file_to_base64(os.path.join(test_files_path, "mask_basic.png"))


@pytest.fixture(scope="session")
def initialize() -> None:
    """Load webui; ensure config exists so opts.data is populated for quality tests."""
    import json
    import os

    from modules.shared_cmd_options import cmd_opts

    config_path = cmd_opts.ui_settings_file
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path) or ".", exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump({"samples_save": True}, f)

    import webui  # noqa: F401
