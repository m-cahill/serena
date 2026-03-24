"""M27 wave 3: util.py and errors.py (mostly uncovered vs prompt_parser)."""
from __future__ import annotations

import sys

import pytest


def test_natural_sort_key_orders_numeric_chunks():
    from modules.util import natural_sort_key

    keys = sorted(["a10", "a2", "a1"], key=natural_sort_key)
    assert keys == ["a1", "a2", "a10"]


def test_listfiles_lists_only_files(tmp_path):
    from modules.util import listfiles

    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "sub").mkdir()
    files = listfiles(str(tmp_path))
    assert len(files) == 2


def test_html_missing_file_returns_empty_string():
    from modules import util as util_mod

    assert util_mod.html("_m27_no_such_html_.html") == ""


def test_walk_files_nonexistent_is_empty():
    from modules.util import walk_files

    assert list(walk_files("/nonexistent_m27_path_xyz", {".txt"})) == []


def test_walk_files_with_extensions(initialize, tmp_path, monkeypatch):
    from modules import shared
    from modules.util import walk_files

    (tmp_path / "keep.txt").write_text("x")
    (tmp_path / "drop.bin").write_bytes(b"\x00")
    monkeypatch.setattr(shared.opts, "list_hidden_files", True)
    found = set(walk_files(str(tmp_path), {".txt"}))
    assert len(found) == 1
    assert str(tmp_path / "keep.txt") in found


def test_walk_files_skips_hidden_dirs_when_disabled(
    initialize, tmp_path, monkeypatch
):
    from modules import shared
    from modules.util import walk_files

    hid = tmp_path / ".hid"
    hid.mkdir()
    (hid / "f.txt").write_text("z")
    (tmp_path / "root.txt").write_text("r")
    monkeypatch.setattr(shared.opts, "list_hidden_files", False)
    found = set(walk_files(str(tmp_path), {".txt"}))
    assert len(found) == 1
    assert all("root.txt" in p for p in found)


def test_truncate_path_under_base(tmp_path):
    from modules.util import truncate_path

    base = tmp_path / "root"
    base.mkdir()
    inner = base / "inner" / "f.txt"
    inner.parent.mkdir(parents=True)
    inner.write_text("z")
    rel = truncate_path(str(inner), str(base))
    assert "inner" in rel.replace("\\", "/")


def test_truncate_path_disjoint_returns_absolute():
    from modules.util import truncate_path

    out = truncate_path("/etc/passwd", "/tmp")
    assert out


def test_topological_sort_chain():
    from modules.util import topological_sort

    deps = {"c": ["b"], "b": ["a"], "a": []}
    order = topological_sort(deps)
    assert order.index("a") < order.index("b") < order.index("c")


def test_mass_file_lister_roundtrip(tmp_path):
    from modules.util import MassFileLister

    p = tmp_path / "g.bin"
    p.write_bytes(b"\x01")
    m = MassFileLister()
    assert m.exists(str(p))
    row = m.find(str(p))
    assert row is not None
    mt, ct = m.mctime(str(p))
    assert mt > 0 and ct > 0
    m.reset()
    assert m.exists(str(p))


def test_mass_file_lister_update_file_entry(tmp_path):
    from modules.util import MassFileLister

    p = tmp_path / "u.txt"
    p.write_text("u")
    m = MassFileLister()
    m.find(str(p))
    m.update_file_entry(str(p))


def test_mass_file_lister_cached_dir_update_missing(tmp_path, capsys):
    from modules.util import MassFileListerCachedDir

    d = MassFileListerCachedDir(str(tmp_path))
    d.update_entry("absent_m27.txt")
    err = capsys.readouterr().out
    assert "absent_m27" in err or "MassFileListerCachedDir" in err


def test_ldm_print_hidden_skips_output(capsys, monkeypatch):
    from modules import shared
    from modules import util as util_mod

    monkeypatch.setattr(shared.opts, "hide_ldm_prints", True)
    util_mod.ldm_print("m27-hidden")
    assert capsys.readouterr().out == ""


def test_format_traceback_and_format_exception():
    import modules.errors as err_mod

    try:
        raise ValueError("m27-err")
    except ValueError:
        _typ, val, tb = sys.exc_info()
        ftb = err_mod.format_traceback(tb)
        assert isinstance(ftb, list)
        fe = err_mod.format_exception(val, tb)
        assert fe["exception"] == "m27-err"


def test_report_and_get_exceptions(capsys):
    import modules.errors as err_mod

    err_mod.exception_records.clear()
    err_mod.report("m27-a\nm27-b", exc_info=False)
    assert "m27-a" in capsys.readouterr().err
    excs = err_mod.get_exceptions()
    assert isinstance(excs, list)


def test_print_error_explanation(capsys):
    import modules.errors as err_mod

    err_mod.exception_records.clear()
    err_mod.print_error_explanation("m27\nlines")
    out = capsys.readouterr().err
    assert "m27" in out


def test_display_value_error(capsys):
    import modules.errors as err_mod

    err_mod.exception_records.clear()
    err_mod.display(ValueError("m27-val"), "m27-task", full_traceback=False)
    assert "ValueError" in capsys.readouterr().err


def test_display_once_dedupes(capsys):
    import modules.errors as err_mod

    err_mod.exception_records.clear()
    err_mod.already_displayed.clear()
    e = RuntimeError("m27-once")
    err_mod.display_once(e, "m27-dedupe-task")
    first = capsys.readouterr().err
    err_mod.display_once(e, "m27-dedupe-task")
    second = capsys.readouterr().err
    assert "RuntimeError" in first
    assert second == ""
