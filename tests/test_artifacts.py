from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import multiagent_elbo.artifacts as artifacts
import numpy as np
import pytest

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import (
    ExperimentConfig,
    canonical_config_json,
    config_sha256,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance


def make_config(root: Path, *, name: str = "finite exact") -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": name, "seed": 20260808},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {"dtype": "float64", "atol": 1e-10, "rtol": 1e-9},
        {
            "root": str(root),
            "collect_diagnostics": True,
            "render_figures": False,
        },
    )


def make_hard_link_or_skip(source: Path, destination: Path) -> None:
    try:
        os.link(source, destination)
    except (NotImplementedError, OSError) as error:
        pytest.skip(f"hard links are unavailable: {error}")


def test_canonical_hash_is_stable_across_source_dictionary_insertion_order(tmp_path: Path):
    first = make_config(tmp_path)
    second = ExperimentConfig.from_dicts(
        {"seed": 20260808, "name": "finite exact"},
        {"retained_interaction_order": 2, "experiment": "finite_exact"},
        {"rtol": 1e-9, "dtype": "float64", "atol": 1e-10},
        {
            "render_figures": False,
            "root": str(tmp_path),
            "collect_diagnostics": True,
        },
    )

    assert canonical_config_json(first) == canonical_config_json(second)
    assert config_sha256(first) == config_sha256(second)


def test_incomplete_run_is_not_overwritten(tmp_path: Path):
    config = make_config(tmp_path)
    provenance = {"source": "test"}

    store = RunStore.create(config, provenance)
    original_config = (store.run_dir / "config.json").read_bytes()

    with pytest.raises(FileExistsError, match="run path already exists"):
        RunStore.create(config, provenance)

    assert (store.run_dir / "config.json").read_bytes() == original_config


def test_create_publishes_an_incomplete_manifest(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})

    manifest = json.loads((store.run_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["complete"] is False
    assert manifest["artifacts"] == {
        "config.json": "complete",
        "manifest.json": "incomplete",
    }


def test_provenance_hash_mismatch_has_no_filesystem_side_effect(tmp_path: Path):
    config = make_config(tmp_path)

    with pytest.raises(
        ValueError, match="provenance config_hash does not match resolved configuration"
    ):
        RunStore.create(config, {"config_hash": "0" * 64})

    assert list(tmp_path.iterdir()) == []


def test_atomic_json_publication_leaves_no_temporary_file(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})

    store.write_json("metrics", {"residual": 0.0})

    assert json.loads((store.run_dir / "metrics.json").read_text(encoding="utf-8")) == {
        "residual": 0.0
    }
    assert not list(store.run_dir.rglob("*.tmp"))


def test_json_artifacts_cannot_overwrite_existing_or_protected_files(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    store.write_json("metrics", {"residual": 0.0})

    for name in ("metrics", "config", "manifest"):
        with pytest.raises(FileExistsError, match=rf"artifact already exists: {name}\.json"):
            store.write_json(name, {"replacement": True})

    assert json.loads((store.run_dir / "metrics.json").read_text(encoding="utf-8")) == {
        "residual": 0.0
    }


def test_npz_publication_uses_requested_filename_without_temporary_suffix(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})

    store.write_npz("arrays", {"values": np.array([1.0, 2.0])})

    with np.load(store.run_dir / "arrays.npz") as archive:
        assert archive["values"].tolist() == [1.0, 2.0]
    assert not list(store.run_dir.rglob("*.tmp"))


def test_npz_artifacts_cannot_overwrite_an_existing_destination(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    store.write_npz("arrays", {"values": np.array([1.0, 2.0])})

    with pytest.raises(FileExistsError, match=r"artifact already exists: arrays\.npz"):
        store.write_npz("arrays", {"values": np.array([3.0, 4.0])})

    with np.load(store.run_dir / "arrays.npz") as archive:
        assert archive["values"].tolist() == [1.0, 2.0]


def test_finalize_rejects_a_missing_declared_artifact_without_completing(
    tmp_path: Path,
):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    store.write_json("metrics", {"residual": 0.0})
    initial_manifest = (store.run_dir / "manifest.json").read_bytes()

    with pytest.raises(
        FileNotFoundError, match=r"declared artifact does not exist: arrays\.npz"
    ):
        store.finalize(["metrics.json", "arrays.npz"])

    assert (store.run_dir / "manifest.json").read_bytes() == initial_manifest


def test_finalize_rejects_deleted_config(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    (store.run_dir / "config.json").unlink()

    with pytest.raises(
        FileNotFoundError, match=r"required artifact does not exist: config\.json"
    ):
        store.finalize([])


@pytest.mark.parametrize("tamper", ["recorded_hash", "resolved_config"])
def test_finalize_rejects_tampered_config_identity(tmp_path: Path, tamper: str):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    config_path = store.run_dir / "config.json"
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if tamper == "recorded_hash":
        payload["config_hash"] = "0" * 64
    else:
        payload["resolved_config"]["run"]["seed"] = 1
    config_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RuntimeError, match="config.json identity does not match run"):
        store.finalize([])


def test_finalize_rejects_an_undeclared_partial_file(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    (store.run_dir / "partial.tmp").write_text("partial", encoding="utf-8")

    with pytest.raises(ValueError, match=r"undeclared run entry: partial\.tmp"):
        store.finalize([])

    manifest = json.loads((store.run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["complete"] is False
    assert "partial.tmp" not in manifest["artifacts"]


def test_finalize_rejects_an_undeclared_directory(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    (store.run_dir / "scratch").mkdir()

    with pytest.raises(ValueError, match="undeclared run entry: scratch"):
        store.finalize([])


@pytest.mark.parametrize(
    "declarations",
    [
        ["metrics.json", "metrics.json"],
        ["metrics.json", "METRICS.json"],
    ],
)
def test_finalize_rejects_portable_duplicate_declarations(
    tmp_path: Path, declarations: list[str]
):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    store.write_json("metrics", {"residual": 0.0})

    with pytest.raises(ValueError, match="duplicate artifact declaration"):
        store.finalize(declarations)


@pytest.mark.parametrize(
    "core_name", ["config.json", "manifest.json", "CONFIG.JSON"]
)
def test_finalize_rejects_core_artifact_declarations(
    tmp_path: Path, core_name: str
):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})

    with pytest.raises(
        ValueError, match=rf"core artifact must not be declared: {core_name}"
    ):
        store.finalize([core_name])


@pytest.mark.parametrize(
    "unsafe_name", ["metrics:stream", "CON", "nul.json", "LPT1.npz"]
)
def test_artifact_writes_reject_ads_and_windows_reserved_names(
    tmp_path: Path, unsafe_name: str
):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})

    with pytest.raises(ValueError, match="invalid artifact filename"):
        store.write_json(unsafe_name, {"value": 1})


def test_finalize_rejects_a_declared_symlink(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    target = tmp_path / "outside.json"
    target.write_text("{}", encoding="utf-8")
    link = store.run_dir / "linked.json"
    try:
        link.symlink_to(target)
    except (NotImplementedError, OSError) as error:
        pytest.skip(f"symlinks are unavailable: {error}")

    with pytest.raises(
        ValueError,
        match=r"artifact must not be a symlink or reparse path: linked\.json",
    ):
        store.finalize(["linked.json"])


def test_finalize_rejects_a_declared_file_with_an_external_hard_link(
    tmp_path: Path,
):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    external = tmp_path / "external.json"
    external.write_text("{}", encoding="utf-8")
    make_hard_link_or_skip(external, store.run_dir / "linked.json")

    with pytest.raises(
        ValueError, match=r"artifact must have exactly one hard link: linked\.json"
    ):
        store.finalize(["linked.json"])


def test_finalize_rejects_an_external_hard_link_to_core_config(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    make_hard_link_or_skip(
        store.run_dir / "config.json", tmp_path / "config-alias.json"
    )

    with pytest.raises(
        ValueError, match=r"artifact must have exactly one hard link: config\.json"
    ):
        store.finalize([])


def test_finalize_rejects_duplicate_file_identity_within_inventory(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    external = tmp_path / "external.json"
    external.write_text("{}", encoding="utf-8")
    make_hard_link_or_skip(external, store.run_dir / "first.json")
    make_hard_link_or_skip(external, store.run_dir / "second.json")

    with pytest.raises(
        ValueError,
        match=r"duplicate artifact file identity: second\.json aliases first\.json",
    ):
        store.finalize(["first.json", "second.json"])


def test_finalize_completes_with_an_accurate_inventory_and_blocks_later_writes(
    tmp_path: Path,
):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})
    store.write_json("metrics", {"residual": 0.0})
    store.write_npz("arrays", {"values": np.array([1.0, 2.0])})

    store.finalize(name for name in ("metrics.json", "arrays.npz"))

    manifest = json.loads((store.run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["complete"] is True
    assert manifest["artifacts"] == {
        "arrays.npz": "complete",
        "config.json": "complete",
        "manifest.json": "complete",
        "metrics.json": "complete",
    }
    with pytest.raises(RuntimeError, match="run is complete"):
        store.write_json("diagnostics", {"value": 1})
    with pytest.raises(RuntimeError, match="run is complete"):
        store.write_npz("diagnostics", {"value": np.array([1.0])})


def test_completed_run_cannot_be_recreated(tmp_path: Path):
    config = make_config(tmp_path)
    provenance = {"source": "test"}
    store = RunStore.create(config, provenance)
    store.finalize([])

    with pytest.raises(FileExistsError, match="complete run exists"):
        RunStore.create(config, provenance)


def test_run_creation_canonicalizes_once_and_hashes_that_exact_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    config = make_config(tmp_path)
    canonical = '{"a":"resolved","z":[2,1]}'
    calls: list[ExperimentConfig] = []

    def record_canonical(argument: ExperimentConfig) -> str:
        calls.append(argument)
        return canonical

    def reject_recanonicalization(_: ExperimentConfig) -> str:
        raise AssertionError("RunStore.create must hash the resolved JSON it already has")

    monkeypatch.setattr(artifacts, "canonical_config_json", record_canonical)
    monkeypatch.setattr(
        artifacts, "config_sha256", reject_recanonicalization, raising=False
    )

    store = RunStore.create(config, {"source": "test"})

    expected_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    config_payload = json.loads((store.run_dir / "config.json").read_text(encoding="utf-8"))
    assert calls == [config]
    assert store.config_hash == expected_hash
    assert config_payload == {
        "config_hash": expected_hash,
        "resolved_config": json.loads(canonical),
    }


def test_manifest_and_config_reference_one_config_hash(tmp_path: Path):
    config = make_config(tmp_path)
    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    provenance = collect_provenance(tmp_path, tmp_path, config_hash, streams)

    store = RunStore.create(config, provenance)

    config_payload = json.loads((store.run_dir / "config.json").read_text(encoding="utf-8"))
    manifest = json.loads((store.run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert config_payload["config_hash"] == config_hash
    assert manifest["config_hash"] == config_hash
    assert manifest["provenance"]["config_hash"] == config_hash
