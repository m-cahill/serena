"""Unit tests for temporary_opts context manager (M05 override isolation seam)."""
from modules import shared
from modules.runtime_utils import temporary_opts


def test_temporary_opts_restores_value(initialize):
    """temporary_opts restores samples_save to original value on exit."""
    original = shared.opts.samples_save

    with temporary_opts({"samples_save": False}):
        assert shared.opts.samples_save is False

    assert shared.opts.samples_save == original


def test_temporary_opts_restore_afterwards_false(initialize):
    """When restore_afterwards=False, value is not restored."""
    original = shared.opts.samples_save
    try:
        with temporary_opts({"samples_save": False}, restore_afterwards=False):
            assert shared.opts.samples_save is False
        assert shared.opts.samples_save is False
    finally:
        shared.opts.samples_save = original


def test_temporary_opts_empty_overrides(initialize):
    """Empty overrides yields without mutation."""
    original = shared.opts.samples_save

    with temporary_opts({}):
        pass

    assert shared.opts.samples_save == original
