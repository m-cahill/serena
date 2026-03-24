"""M27: exercise previously cold paths in images.py and extras.py."""
from __future__ import annotations

import torch
from PIL import Image


def test_extras_run_pnginfo_none():
    from modules import extras

    assert extras.run_pnginfo(None) == ("", "", "")


def test_extras_to_half_dtype_paths():
    from modules import extras

    f = torch.tensor([1.0], dtype=torch.float32)
    assert extras.to_half(f, False) is f
    assert extras.to_half(f, True).dtype == torch.float16
    h = f.half()
    assert extras.to_half(h, True).dtype == torch.float16


def test_extras_read_metadata_missing_checkpoints(initialize):
    from modules import extras

    assert extras.read_metadata("__m27a__", "__m27b__", "__m27c__") == "{}"


def test_images_sanitize_filename_part(initialize):
    from modules import images

    out = images.sanitize_filename_part("a b")
    assert out is not None
    assert " " not in out


def test_images_scheduler_strings(initialize):
    from modules import images

    sch = images.get_scheduler_str("Euler a", "Automatic")
    assert isinstance(sch, str) and len(sch) > 0
    both = images.get_sampler_scheduler_str("Euler a", "Automatic")
    assert "Euler" in both


def test_images_get_sampler_scheduler_named(initialize):
    from modules import images

    class _P:
        sampler_name = "Euler a"
        scheduler = "Automatic"

    r = images.get_sampler_scheduler(_P(), True)
    assert r is not images.NOTHING_AND_SKIP_PREVIOUS_TEXT


def test_images_image_grid_one(initialize):
    from modules import images

    im = Image.new("RGB", (12, 10), color=(1, 2, 3))
    grid = images.image_grid([im], batch_size=1, rows=1)
    assert grid.size[0] >= 12 and grid.size[1] >= 10


def test_images_image_grid_two_auto_rows(initialize):
    from modules import images

    a = Image.new("RGB", (8, 8), color=1)
    b = Image.new("RGB", (8, 8), color=2)
    grid = images.image_grid([a, b], batch_size=2, rows=None)
    assert grid.size[0] > 0


def test_images_split_and_combine_grid(initialize):
    from modules import images

    im = Image.new("RGB", (120, 80), color=(5, 5, 5))
    g = images.split_grid(im, tile_w=50, tile_h=50, overlap=10)
    assert g.tile_count >= 1
    merged = images.combine_grid(g)
    assert merged.mode == "RGB"
    assert merged.size == im.size


def test_images_read_info_blank(initialize):
    from modules import images

    im = Image.new("RGB", (6, 6), color=0)
    gen, items = images.read_info_from_image(im)
    assert gen is None or isinstance(gen, str)
    assert isinstance(items, dict)


def test_images_fix_png_transparency_and_flatten(initialize):
    from modules import images

    im = Image.new("RGBA", (6, 6), color=(10, 20, 30, 200))
    images.fix_png_transparency(im)
    rgb = Image.new("RGB", (5, 5), (1, 2, 3))
    flat = images.flatten(rgb, (0, 0, 0))
    assert flat.mode == "RGB"


def test_images_get_next_sequence_number(tmp_path):
    from modules import images

    assert images.get_next_sequence_number(str(tmp_path), "") == 0
    (tmp_path / "0000.png").write_bytes(b"x")
    assert images.get_next_sequence_number(str(tmp_path), "") >= 1
    (tmp_path / "seq-0000.png").write_bytes(b"y")
    assert images.get_next_sequence_number(str(tmp_path), "seq") >= 1


def test_images_read_png_file(tmp_path, initialize):
    from modules import images

    im = Image.new("RGB", (5, 5), color=2)
    p = tmp_path / "m27.png"
    im.save(p)
    loaded = images.read(str(p))
    assert loaded.size == (5, 5)
