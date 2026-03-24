"""M27: hashes.calculate_sha256 (stdlib path)."""
from __future__ import annotations

import hashlib


def test_calculate_sha256_matches_digest(initialize, tmp_path):
    from modules.hashes import calculate_sha256

    p = tmp_path / "blob.bin"
    data = b"serena-m27-coverage"
    p.write_bytes(data)
    expected = hashlib.sha256(data).hexdigest()
    assert calculate_sha256(str(p)) == expected
