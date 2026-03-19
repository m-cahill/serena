"""M18 contract tests: process_images_inner delegates decode/postprocess/save to decode_runtime."""

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_processing_source() -> str:
    return (_repo_root() / "modules" / "processing.py").read_text(encoding="utf-8")


def _read_decode_runtime_source() -> str:
    return (_repo_root() / "modules" / "runtime" / "decode_runtime.py").read_text(encoding="utf-8")


def test_decode_runtime_module_exports():
    """decode_runtime source defines decode, postprocess, and save entrypoints."""
    src = _read_decode_runtime_source()
    assert "def decode_latents" in src
    assert "def decode_latent_batch" in src
    assert "def postprocess_face_restore_row" in src
    assert "def postprocess_images_for_row" in src
    assert "def save_outputs_for_row" in src
    assert "def save_outputs_grid" in src


def test_process_images_inner_delegates_to_decode_runtime():
    """process_images_inner routes decode/postprocess/save through decode_runtime."""
    source = _read_processing_source()
    assert "decode_runtime.decode_latents" in source
    assert "decode_runtime.postprocess_face_restore_row" in source
    assert "decode_runtime.postprocess_images_for_row" in source
    assert "decode_runtime.save_outputs_for_row" in source
    assert "decode_runtime.save_outputs_grid" in source


def test_process_images_inner_decode_runtime_call_order():
    """Stage order: decode → per-row postprocess/save → grid save (textual contract)."""
    source = _read_processing_source()
    markers = [
        "decode_runtime.decode_latents",
        "decode_runtime.postprocess_face_restore_row",
        "decode_runtime.postprocess_images_for_row",
        "decode_runtime.save_outputs_for_row",
        "decode_runtime.save_outputs_grid",
    ]
    positions = [source.index(m) for m in markers]
    assert positions == sorted(positions)


def test_decode_latents_source_preserves_stack_and_normalize():
    """Narrow equivalence (static): same stack + (x+1)/2 clamp as former process_images_inner path."""
    src = _read_decode_runtime_source()
    assert "torch.stack(x_samples_ddim).float()" in src
    assert "torch.clamp((x_samples_ddim + 1.0) / 2.0, min=0.0, max=1.0)" in src
