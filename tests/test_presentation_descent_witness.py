import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WITNESS = (
    ROOT
    / "docs/derivations/2026-08-13-finite-presentation-descent-joint-fisher"
    / "evidence/exact_finite_witness.py"
)


def test_exact_finite_presentation_descent_witness(capsys) -> None:
    specification = importlib.util.spec_from_file_location(
        "exact_finite_presentation_descent_witness", WITNESS
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    assert module.main() == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["bsc"] == {
        "a": "1/10",
        "b": "1/8",
        "fisher_gap": "225/28",
        "full_fisher": "100/7",
        "retained_crossover": "1/5",
        "retained_fisher": "25/4",
    }
    assert payload["failure_certificate"] == {
        "delta": "5/12",
        "full_l0_diagonal": ["16/3", "9/2", "0"],
        "full_lplus_diagonal": ["16/3", "9/2", "25/6"],
        "intervention_match_probability": "2/3",
        "null_kl_exact": "log(25/24)/2",
        "retained_tensor": [
            ["16/35", "24/35", "0"],
            ["24/35", "36/35", "0"],
            ["0", "0", "0"],
        ],
    }
    assert payload["categorical_lifts"]["product_metric"] == [["4", "0"], ["0", "4"]]
    assert payload["categorical_lifts"]["correlated_metric"] == [
        ["256/63", "-32/63"],
        ["-32/63", "256/63"],
    ]
    assert payload["categorical_lifts"]["metric_difference_eigenvalues"] == ["-4/9", "4/7"]
    assert payload["categorical_lifts"]["kl_exact"] == "log(64/63)/2"
    assert payload["categorical_lifts"]["correlated_vfe"] > 0
