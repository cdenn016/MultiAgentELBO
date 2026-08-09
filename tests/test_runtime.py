from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

import scipy

import multiagent_elbo.runtime as runtime
from multiagent_elbo.runtime import RngStreams, collect_provenance


def test_equal_seeds_produce_identical_named_stream_draws():
    first = RngStreams.from_seed(314159)
    second = RngStreams.from_seed(314159)

    for name in ("problem", "recognition", "controls", "figures"):
        assert getattr(first, name).integers(0, 2**31, size=8).tolist() == getattr(
            second, name
        ).integers(0, 2**31, size=8).tolist()


def test_named_streams_do_not_share_the_same_initial_draws():
    streams = RngStreams.from_seed(314159)

    draws = {
        name: tuple(getattr(streams, name).integers(0, 2**31, size=8))
        for name in ("problem", "recognition", "controls", "figures")
    }

    assert len(set(draws.values())) == 4


def test_provenance_records_scipy_and_exact_input_hash_bindings(
    tmp_path: Path, monkeypatch
):
    theory = tmp_path / "Theory"
    theory.mkdir()
    (theory / "main.tex").write_text("theory", encoding="utf-8")
    config_hash = "a" * 64
    monkeypatch.setattr(runtime, "_git_output", lambda *_args: "1" * 40)
    monkeypatch.setattr(runtime, "_git_status_bytes", lambda *_args: b"")

    provenance = collect_provenance(
        tmp_path, theory, config_hash, RngStreams.from_seed(7)
    )

    assert provenance["scipy_version"] == scipy.__version__
    assert provenance["theory_exists"] is True
    assert provenance["theory_sha256"] == runtime._tree_sha256(theory)
    assert provenance["input_hashes"] == {
        "resolved_config_sha256": config_hash,
        "theory_tree_sha256": provenance["theory_sha256"],
    }
    assert tuple(provenance["input_hashes"]) == (
        "resolved_config_sha256",
        "theory_tree_sha256",
    )


def test_git_status_digest_is_sha256_of_exact_nul_delimited_porcelain_bytes(
    tmp_path: Path, monkeypatch
):
    raw_status = b" M src/a.py\0?? notes/new.txt\0"
    monkeypatch.setattr(runtime, "_git_output", lambda *_args: "2" * 40)
    monkeypatch.setattr(runtime, "_git_status_bytes", lambda *_args: raw_status)

    provenance = collect_provenance(
        tmp_path, tmp_path / "missing-theory", "b" * 64, RngStreams.from_seed(8)
    )

    assert provenance["git_dirty"] is True
    assert provenance["git_status_format"] == (
        "git-status-porcelain-v1-z-untracked-files-all"
    )
    assert provenance["git_status_sha256"] == hashlib.sha256(raw_status).hexdigest()


def test_clean_git_status_has_false_dirty_flag_and_empty_stream_digest(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setattr(runtime, "_git_output", lambda *_args: "3" * 40)
    monkeypatch.setattr(runtime, "_git_status_bytes", lambda *_args: b"")

    provenance = collect_provenance(
        tmp_path, tmp_path / "missing-theory", "c" * 64, RngStreams.from_seed(9)
    )

    assert provenance["git_dirty"] is False
    assert provenance["git_status_sha256"] == hashlib.sha256(b"").hexdigest()


def test_non_git_and_missing_theory_are_explicit_and_side_effect_free(
    tmp_path: Path, monkeypatch
):
    repo = tmp_path / "not-created-repo"
    theory = tmp_path / "not-created-theory"
    monkeypatch.setattr(runtime, "_git_output", lambda *_args: None)
    monkeypatch.setattr(runtime, "_git_status_bytes", lambda *_args: None)

    provenance = collect_provenance(
        repo, theory, "d" * 64, RngStreams.from_seed(10)
    )

    assert provenance["git_commit"] is None
    assert provenance["git_dirty"] is None
    assert provenance["git_status_sha256"] is None
    assert provenance["theory_exists"] is False
    assert provenance["theory_sha256"] is None
    assert provenance["input_hashes"]["theory_tree_sha256"] is None
    assert not repo.exists()
    assert not theory.exists()


def test_tree_digest_is_stable_across_creation_order_and_binds_names_and_bytes(
    tmp_path: Path,
):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    (first / "b.tex").write_text("B", encoding="utf-8")
    (first / "a.tex").write_text("A", encoding="utf-8")
    (second / "a.tex").write_text("A", encoding="utf-8")
    (second / "b.tex").write_text("B", encoding="utf-8")

    original = runtime._tree_sha256(first)

    assert original == runtime._tree_sha256(second)
    (second / "b.tex").rename(second / "c.tex")
    assert runtime._tree_sha256(second) != original
    (second / "c.tex").rename(second / "b.tex")
    (second / "b.tex").write_text("changed", encoding="utf-8")
    assert runtime._tree_sha256(second) != original


def test_git_status_capture_uses_stable_binary_porcelain_command(
    tmp_path: Path, monkeypatch
):
    calls: list[tuple[list[str], dict[str, object]]] = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, stdout=b"?? z.txt\0", stderr=b"")

    monkeypatch.setattr(runtime.subprocess, "run", fake_run)

    assert runtime._git_status_bytes(tmp_path) == b"?? z.txt\0"
    assert calls == [
        (
            [
                "git",
                "-C",
                str(tmp_path),
                "status",
                "--porcelain=v1",
                "-z",
                "--untracked-files=all",
            ],
            {"capture_output": True, "check": False},
        )
    ]
