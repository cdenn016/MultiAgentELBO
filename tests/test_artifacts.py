from __future__ import annotations

import json
from pathlib import Path

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


def test_completed_run_is_not_overwritten(tmp_path: Path):
    config = make_config(tmp_path)
    provenance = {"source": "test"}

    RunStore.create(config, provenance)

    with pytest.raises(FileExistsError, match="complete run exists"):
        RunStore.create(config, provenance)


def test_atomic_json_publication_leaves_no_temporary_file(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})

    store.write_json("metrics", {"residual": 0.0})

    assert json.loads((store.run_dir / "metrics.json").read_text(encoding="utf-8")) == {
        "residual": 0.0
    }
    assert not list(store.run_dir.rglob("*.tmp"))


def test_npz_publication_uses_requested_filename_without_temporary_suffix(tmp_path: Path):
    store = RunStore.create(make_config(tmp_path), {"source": "test"})

    store.write_npz("arrays", {"values": np.array([1.0, 2.0])})

    with np.load(store.run_dir / "arrays.npz") as archive:
        assert archive["values"].tolist() == [1.0, 2.0]
    assert not list(store.run_dir.rglob("*.tmp"))


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
