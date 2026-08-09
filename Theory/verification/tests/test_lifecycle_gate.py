"""Real, monotone Git-history RED contract for S/E/C/W lifecycle gates."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import shutil
import subprocess
from pathlib import Path

import pytest


GATE_PATH = Path(__file__).resolve().parents[1] / "lifecycle_gate.py"
FIXED_GIT_EXECUTABLE = Path(r"C:\Program Files\Git\cmd\git.exe")

E_TO_C_PATHS = (
    "docs/derivations/closure-attestation.json",
    "docs/derivations/release.json",
)

PRODUCTION_TASK_PLAN = (
    "docs/superpowers/plans/2026-08-03-gauge-vfe-rg-review-remediation.md"
)
PRODUCTION_TASK_DESIGN = (
    "docs/superpowers/specs/2026-08-03-gauge-vfe-rg-review-remediation-design.md"
)
PRODUCTION_EVIDENCE_PATHS = (
    "manuscripts/gauge_vfe_rg/verification/current-results.json",
    "manuscripts/gauge_vfe_rg/main.pdf",
    "docs/derivations/2026-08-03-gauge-vfe-rg-remediation/construction-or-strongest-theorem.md",
    "docs/derivations/2026-08-03-gauge-vfe-rg-remediation/counterexample-register.md",
    "docs/derivations/2026-08-03-gauge-vfe-rg-remediation/adversarial-report.json",
)
PRODUCTION_WIKI_PATHS = (
    "sources/manuscripts/gauge-vfe-rg-cross-scale-operator-theory-2026-08-03.md",
    "wiki/projects/Gauge-Theoretic Multi-Agent VFE Model.md",
    "wiki/concepts/Coarse Graining.md",
    "wiki/concepts/Renormalization group flow.md",
    "wiki/concepts/Renormalization-group flow of beliefs.md",
    "index.md",
    "log.md",
)
PRODUCTION_CLOSURE_PATHS = (
    "docs/derivations/2026-08-03-gauge-vfe-rg-remediation/release.json",
    "docs/derivations/2026-08-03-gauge-vfe-rg-remediation/final-report.md",
    "docs/reviews/2026-08-03-gauge-vfe-rg-remediation-closure-attestation.md",
    "docs/reviews/2026-08-03-gauge-vfe-rg-remediation-verification-ledger.json",
)
PRODUCTION_MANDATORY_PATHS = (
    "manuscripts/gauge_vfe_rg/main.tex",
    "manuscripts/gauge_vfe_rg/01_introduction.tex",
    "manuscripts/gauge_vfe_rg/02_geometry.tex",
    "manuscripts/gauge_vfe_rg/03_probability.tex",
    "manuscripts/gauge_vfe_rg/04_generative.tex",
    "manuscripts/gauge_vfe_rg/05_elbo.tex",
    "manuscripts/gauge_vfe_rg/05a_expfamily.tex",
    "manuscripts/gauge_vfe_rg/05b_local_collective_elbo.tex",
    "manuscripts/gauge_vfe_rg/05c_pullback_geometry.tex",
    "manuscripts/gauge_vfe_rg/05d_relational_inference.tex",
    "manuscripts/gauge_vfe_rg/06_general_coarsegraining.tex",
    "manuscripts/gauge_vfe_rg/06_gaussian.tex",
    "manuscripts/gauge_vfe_rg/06a_generative_gaussian.tex",
    "manuscripts/gauge_vfe_rg/07_general_renormalization.tex",
    "manuscripts/gauge_vfe_rg/07_restrictions.tex",
    "manuscripts/gauge_vfe_rg/07b_agent_network_rg.tex",
    "manuscripts/gauge_vfe_rg/08_infogeometry.tex",
    "manuscripts/gauge_vfe_rg/09_coarsegraining.tex",
    "manuscripts/gauge_vfe_rg/10_renormalization.tex",
    "manuscripts/gauge_vfe_rg/11_obstructions.tex",
    "manuscripts/gauge_vfe_rg/12_philosophy.tex",
    "manuscripts/gauge_vfe_rg/appendix_claim_ledger.tex",
    "manuscripts/gauge_vfe_rg/appendix_notation.tex",
    "manuscripts/gauge_vfe_rg/appendix_numerical_provenance.tex",
    "manuscripts/gauge_vfe_rg/SPEC.md",
    "manuscripts/gauge_vfe_rg/build.ps1",
    "manuscripts/references.bib",
    "manuscripts/scientific_report.sty",
    "manuscripts/gauge_vfe_rg/verification/claims.json",
    "manuscripts/gauge_vfe_rg/verification/run_checks.py",
    "manuscripts/gauge_vfe_rg/verification/requirements.txt",
    "manuscripts/gauge_vfe_rg/verification/VERIFICATION.md",
    "manuscripts/gauge_vfe_rg/verification/result.schema.json",
    "manuscripts/gauge_vfe_rg/verification/manifest-policy.json",
    "manuscripts/gauge_vfe_rg/verification/lifecycle_gate.py",
    "manuscripts/gauge_vfe_rg/verification/build_audit.py",
    "manuscripts/gauge_vfe_rg/verification/build_bootstrap_reference.ps1.txt",
    "manuscripts/gauge_vfe_rg/verification/build_bootstrap_transport.txt",
    "manuscripts/gauge_vfe_rg/verification/tests/test_factorization_gap.py",
    "manuscripts/gauge_vfe_rg/verification/tests/test_runner_cli.py",
    "manuscripts/gauge_vfe_rg/verification/tests/test_manifest_binding.py",
    "manuscripts/gauge_vfe_rg/verification/tests/test_lifecycle_gate.py",
    "manuscripts/gauge_vfe_rg/verification/tests/test_build_audit.py",
    "manuscripts/gauge_vfe_rg/verification/tests/test_build_bootstrap.py",
    PRODUCTION_TASK_PLAN,
    PRODUCTION_TASK_DESIGN,
)


class MissingGate:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, *_args, **_kwargs):
        return [] if self.name == "parse_name_status_z" else self


def git(repo: Path, *args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=False)
    assert completed.returncode == 0, f"DEFECT [git fixture]: git {' '.join(args)} failed: {completed.stderr}"
    return completed.stdout.strip()


def commit(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def commit_index(repo: Path, message: str) -> str:
    git(
        repo,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-m",
        message,
    )
    return git(repo, "rev-parse", "HEAD")


def empty_commit(repo: Path, message: str) -> str:
    git(
        repo,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "--allow-empty",
        "-m",
        message,
    )
    return git(repo, "rev-parse", "HEAD")


def commit_tree(repo: Path, tree: str, parent: str, message: str) -> str:
    return commit_tree_with_parents(repo, tree, (parent,), message)


def commit_tree_with_parents(
    repo: Path,
    tree: str,
    parents: tuple[str, ...],
    message: str,
) -> str:
    arguments = [
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit-tree",
        tree,
    ]
    for parent in parents:
        arguments.extend(("-p", parent))
    arguments.extend(("-m", message))
    return git(
        repo,
        *arguments,
    )


def deep_protected_side_dag(
    repo: Path,
    wiki_revision: str,
    drift: str,
) -> tuple[str, str, str]:
    """Build unrelated root -> protected attack -> exact-W restoration."""

    protected = "manuscripts/gauge_vfe_rg/verification/current-results.json"
    checkout(repo, f"deep-protected-side-{drift}", wiki_revision)
    if drift == "bytes":
        write(repo, protected, "deep side-DAG protected byte drift\n")
        attack_tree_source = commit(repo, "deep protected byte tree")
    elif drift == "type":
        protected_blob = git(repo, "rev-parse", f"{wiki_revision}:{protected}")
        git(
            repo,
            "update-index",
            "--cacheinfo",
            f"120000,{protected_blob},{protected}",
        )
        attack_tree_source = commit_index(repo, "deep protected type tree")
    else:
        (repo / protected).unlink()
        attack_tree_source = commit(repo, "deep protected existence tree")

    clean_tree = git(repo, "rev-parse", f"{wiki_revision}^{{tree}}")
    unrelated_root = commit_tree_with_parents(
        repo,
        clean_tree,
        (),
        "unrelated W-clean root",
    )
    attacked = commit_tree(
        repo,
        git(repo, "rev-parse", f"{attack_tree_source}^{{tree}}"),
        unrelated_root,
        f"deep protected {drift} attack",
    )
    restored = commit_tree(
        repo,
        clean_tree,
        attacked,
        f"deep protected {drift} restoration",
    )
    return attacked, restored, protected


def write(repo: Path, relative: str, text: str = "x\n") -> None:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def checkout(repo: Path, branch: str, revision: str) -> None:
    git(repo, "checkout", "-B", branch, revision)


def history(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    repo = tmp_path / "history"
    repo.mkdir()
    git(repo, "init")
    write(repo, "fixtures/source.txt")
    revisions = {"S": commit(repo, "source")}
    checkout(repo, "evidence", revisions["S"])
    write(repo, "manuscripts/gauge_vfe_rg/verification/current-results.json", "{}\n")
    write(repo, "docs/derivations/evidence/numerics.json", "{}\n")
    revisions["E"] = commit(repo, "evidence")
    checkout(repo, "closure", revisions["E"])
    for path in E_TO_C_PATHS:
        write(repo, path, "{}\n")
    revisions["C"] = commit(repo, "closure")
    checkout(repo, "wiki", revisions["C"])
    write(repo, "sources/manuscripts/gauge-vfe-rg-cross-scale-operator-theory-2026-08-03.md")
    write(repo, "wiki/concepts/Coarse Graining.md")
    write(repo, "index.md")
    write(repo, "log.md")
    revisions["W"] = commit(repo, "wiki")
    return repo, revisions


def production_history(
    tmp_path: Path,
    *,
    missing_mandatory: str | None = None,
    missing_evidence: str | None = None,
    missing_closure: str | None = None,
    preseed_wiki: bool = False,
    changed_wiki_paths: tuple[str, ...] = PRODUCTION_WIKI_PATHS,
) -> tuple[Path, dict[str, str]]:
    repo = tmp_path / "production-history"
    repo.mkdir()
    git(repo, "init")
    for index, path in enumerate(PRODUCTION_MANDATORY_PATHS, start=1):
        if path != missing_mandatory:
            write(repo, path, f"mandatory source {index}: {path}\n")
    if preseed_wiki:
        for index, path in enumerate(PRODUCTION_WIKI_PATHS, start=1):
            write(repo, path, f"preexisting wiki {index}: {path}\n")
    revisions = {"S": commit(repo, "production source")}

    checkout(repo, "production-evidence", revisions["S"])
    for index, path in enumerate(PRODUCTION_EVIDENCE_PATHS, start=1):
        if path != missing_evidence:
            write(repo, path, f"production evidence {index}: {path}\n")
    revisions["E"] = commit(repo, "production evidence")

    checkout(repo, "production-closure", revisions["E"])
    for index, path in enumerate(PRODUCTION_CLOSURE_PATHS, start=1):
        if path != missing_closure:
            write(repo, path, f"production closure {index}: {path}\n")
    revisions["C"] = commit(repo, "production closure")

    checkout(repo, "production-wiki", revisions["C"])
    for index, path in enumerate(changed_wiki_paths, start=1):
        write(repo, path, f"production wiki W {index}: {path}\n")
    revisions["W"] = commit(repo, "production wiki")
    return repo, revisions


def production_history_with_status(
    tmp_path: Path, boundary: str, status: str
) -> tuple[Path, dict[str, str]]:
    """Create a production-shaped history with one forbidden phase status."""

    phase_paths = {
        "S..E": PRODUCTION_EVIDENCE_PATHS,
        "E..C": PRODUCTION_CLOSURE_PATHS,
        "C..W": PRODUCTION_WIKI_PATHS,
    }
    repo = tmp_path / f"production-{boundary.replace('.', '-')}-{status}"
    repo.mkdir()
    git(repo, "init")
    for index, path in enumerate(PRODUCTION_MANDATORY_PATHS, start=1):
        write(repo, path, f"mandatory source {index}: {path}\n")
    source_path = phase_paths[boundary][0]
    source_text = f"unique {boundary} {status} source\n"
    write(repo, source_path, source_text)
    revisions = {"S": commit(repo, "production source with phase seed")}

    phase_specs = (
        ("S..E", "E", "production-evidence"),
        ("E..C", "C", "production-closure"),
        ("C..W", "W", "production-wiki"),
    )
    older_label = "S"
    for phase_boundary, newer_label, branch in phase_specs:
        checkout(repo, branch, revisions[older_label])
        paths = phase_paths[phase_boundary]
        if phase_boundary != boundary:
            for index, path in enumerate(paths, start=1):
                write(repo, path, f"normal {phase_boundary} {index}: {path}\n")
            revisions[newer_label] = commit(repo, f"normal {phase_boundary}")
        else:
            if status == "D":
                (repo / paths[0]).unlink()
                for index, path in enumerate(paths[1:], start=2):
                    write(repo, path, f"destination {index}: {path}\n")
            elif status == "R":
                (repo / paths[0]).unlink()
                write(repo, paths[1], source_text)
                for index, path in enumerate(paths[2:], start=3):
                    write(repo, path, f"destination {index}: {path}\n")
            elif status == "C":
                write(repo, paths[1], source_text)
                for index, path in enumerate(paths[2:], start=3):
                    write(repo, path, f"destination {index}: {path}\n")
            elif status == "T":
                for index, path in enumerate(paths[1:], start=2):
                    write(repo, path, f"destination {index}: {path}\n")
                git(repo, "add", "-A")
                git(
                    repo,
                    "update-index",
                    "--add",
                    "--cacheinfo",
                    f"160000,{revisions[older_label]},{paths[0]}",
                )
                revisions[newer_label] = commit_index(
                    repo, f"forbidden {status} at {phase_boundary}"
                )
                older_label = newer_label
                continue
            else:
                raise AssertionError(f"unsupported fixture status: {status}")
            revisions[newer_label] = commit(
                repo, f"forbidden {status} at {phase_boundary}"
            )
        older_label = newer_label
    return repo, revisions


def gate_module():
    if not GATE_PATH.is_file():
        return None
    spec = importlib.util.spec_from_file_location("lifecycle_gate_contract", GATE_PATH)
    assert spec and spec.loader, "DEFECT [lifecycle module]: lifecycle_gate.py must be importable"
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def require_gate(name: str, defect: str):
    loaded = gate_module()
    value = getattr(loaded, name, None) if loaded is not None else None
    return value if callable(value) else MissingGate(name)


def test_gate_accepts_monotone_real_allowed_s_e_c_w_history_and_authorized_source_note(tmp_path: Path):
    repo, revisions = history(tmp_path)
    outcome = require_gate("validate_lifecycle", "real S/E/C/W gate")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )
    assert getattr(outcome, "ok", None) is True, "DEFECT [real S/E/C/W gate]: allowed monotone history was rejected"


@pytest.mark.parametrize("boundary", ["S..E", "E..C", "C..W"])
def test_lifecycle_rejects_forbidden_change_restored_inside_each_phase(
    tmp_path: Path,
    boundary: str,
):
    repo, valid = history(tmp_path)
    older_label, newer_label = boundary.split("..")
    checkout(repo, f"phase-restore-{older_label.lower()}", valid[older_label])
    write(repo, "fixtures/source.txt", f"forbidden transient {boundary}\n")
    changed = commit(repo, f"forbidden transient {boundary}")
    restored = commit_tree(
        repo,
        git(repo, "rev-parse", f"{valid[older_label]}^{{tree}}"),
        changed,
        f"restore phase baseline {boundary}",
    )
    revised = dict(valid)
    endpoint = commit_tree(
        repo,
        git(repo, "rev-parse", f"{valid[newer_label]}^{{tree}}"),
        restored,
        f"rebuild {newer_label}",
    )
    revised[newer_label] = endpoint
    previous = endpoint
    for label in {"E": ("C", "W"), "C": ("W",), "W": ()}[newer_label]:
        previous = commit_tree(
            repo,
            git(repo, "rev-parse", f"{valid[label]}^{{tree}}"),
            previous,
            f"rebuild {label}",
        )
        revised[label] = previous
    git(repo, "update-ref", "HEAD", revised["W"])

    outcome = require_gate("validate_lifecycle", "phase history purity")(
        repo,
        revised["S"],
        revised["E"],
        revised["C"],
        revised["W"],
        test_fixture=True,
    )

    assert outcome.ok is False and any(
        boundary in finding and changed in finding
        for finding in outcome.findings
    ), f"DEFECT [{boundary} history]: restored forbidden change passed"


@pytest.mark.parametrize(
    "scenario",
    ("forbidden-path", "protected-bytes", "protected-type", "protected-existence"),
)
def test_production_phase_rejects_off_subgraph_merge_parent_drift_restored_at_merge(
    tmp_path: Path,
    scenario: str,
):
    repo, valid = production_history(tmp_path)
    protected = "manuscripts/gauge_vfe_rg/main.tex"
    checkout(repo, f"off-subgraph-{scenario}", valid["S"])
    if scenario == "forbidden-path":
        attacked_path = "forbidden/off-subgraph-parent.txt"
        write(repo, attacked_path, "forbidden parent-only path\n")
        side_descendant = commit(repo, "off-subgraph forbidden path tree")
    elif scenario == "protected-bytes":
        attacked_path = protected
        write(repo, protected, "off-subgraph protected byte drift\n")
        side_descendant = commit(repo, "off-subgraph protected byte tree")
    elif scenario == "protected-type":
        attacked_path = protected
        protected_blob = git(repo, "rev-parse", f'{valid["S"]}:{protected}')
        git(
            repo,
            "update-index",
            "--cacheinfo",
            f"120000,{protected_blob},{protected}",
        )
        side_descendant = commit_index(repo, "off-subgraph protected type tree")
    else:
        attacked_path = protected
        (repo / protected).unlink()
        side_descendant = commit(repo, "off-subgraph protected existence tree")

    side_parent = commit_tree_with_parents(
        repo,
        git(repo, "rev-parse", f"{side_descendant}^{{tree}}"),
        (),
        f"unrelated root parent with {scenario}",
    )
    revised = dict(valid)
    revised["E"] = commit_tree_with_parents(
        repo,
        git(repo, "rev-parse", f'{valid["E"]}^{{tree}}'),
        (valid["E"], side_parent),
        f"merge and restore {scenario} at E",
    )
    revised["C"] = commit_tree(
        repo,
        git(repo, "rev-parse", f'{valid["C"]}^{{tree}}'),
        revised["E"],
        "rebuild C after off-subgraph merge",
    )
    revised["W"] = commit_tree(
        repo,
        git(repo, "rev-parse", f'{valid["W"]}^{{tree}}'),
        revised["C"],
        "rebuild W after off-subgraph merge",
    )
    git(repo, "update-ref", "HEAD", revised["W"])

    outcome = require_gate("validate_lifecycle", "off-subgraph merge-parent edge")(
        repo,
        revised["S"],
        revised["E"],
        revised["C"],
        revised["W"],
    )

    assert outcome.ok is False and any(
        side_parent in finding
        and revised["E"] in finding
        and attacked_path in finding
        and "phase-history edge violation" in finding
        for finding in outcome.findings
    ), (
        "DEFECT [off-subgraph merge-parent edge]: restored parent drift passed: "
        f"scenario={scenario} findings={outcome.findings}"
    )


@pytest.mark.parametrize(
    "scenario",
    ("forbidden-path", "protected-bytes", "protected-type", "protected-existence"),
)
def test_production_phase_rejects_deep_off_subgraph_drift_restored_before_merge(
    tmp_path: Path,
    scenario: str,
):
    repo, valid = production_history(tmp_path)
    protected = "manuscripts/gauge_vfe_rg/main.tex"
    checkout(repo, f"deep-off-subgraph-{scenario}", valid["S"])
    if scenario == "forbidden-path":
        attacked_path = "forbidden/deep-off-subgraph.txt"
        write(repo, attacked_path, "forbidden deep side-DAG path\n")
        attack_tree_source = commit(repo, "deep off-subgraph forbidden tree")
    elif scenario == "protected-bytes":
        attacked_path = protected
        write(repo, protected, "deep off-subgraph protected byte drift\n")
        attack_tree_source = commit(repo, "deep off-subgraph protected byte tree")
    elif scenario == "protected-type":
        attacked_path = protected
        protected_blob = git(repo, "rev-parse", f'{valid["S"]}:{protected}')
        git(
            repo,
            "update-index",
            "--cacheinfo",
            f"120000,{protected_blob},{protected}",
        )
        attack_tree_source = commit_index(repo, "deep off-subgraph protected type tree")
    else:
        attacked_path = protected
        (repo / protected).unlink()
        attack_tree_source = commit(repo, "deep off-subgraph protected existence tree")

    clean_tree = git(repo, "rev-parse", f'{valid["S"]}^{{tree}}')
    unrelated_root = commit_tree_with_parents(
        repo,
        clean_tree,
        (),
        "unrelated clean phase root",
    )
    attacked = commit_tree(
        repo,
        git(repo, "rev-parse", f"{attack_tree_source}^{{tree}}"),
        unrelated_root,
        f"deep side-DAG attack {scenario}",
    )
    restored = commit_tree(
        repo,
        clean_tree,
        attacked,
        f"deep side-DAG restore {scenario}",
    )

    revised = dict(valid)
    revised["E"] = commit_tree_with_parents(
        repo,
        git(repo, "rev-parse", f'{valid["E"]}^{{tree}}'),
        (valid["E"], restored),
        f"merge restored deep side-DAG {scenario}",
    )
    revised["C"] = commit_tree(
        repo,
        git(repo, "rev-parse", f'{valid["C"]}^{{tree}}'),
        revised["E"],
        "rebuild C after deep off-subgraph merge",
    )
    revised["W"] = commit_tree(
        repo,
        git(repo, "rev-parse", f'{valid["W"]}^{{tree}}'),
        revised["C"],
        "rebuild W after deep off-subgraph merge",
    )
    git(repo, "update-ref", "HEAD", revised["W"])

    outcome = require_gate("validate_lifecycle", "deep off-subgraph phase DAG")(
        repo,
        revised["S"],
        revised["E"],
        revised["C"],
        revised["W"],
    )

    assert outcome.ok is False and any(
        attacked in finding
        and restored in finding
        and attacked_path in finding
        and "phase-history edge violation" in finding
        for finding in outcome.findings
    ), (
        "DEFECT [deep off-subgraph phase DAG]: A-to-B drift restoration passed: "
        f"scenario={scenario} findings={outcome.findings}"
    )


@pytest.mark.parametrize("boundary", ["S..E", "E..C", "C..W"])
def test_production_lifecycle_rejects_allowed_add_delete_readd_inside_phase(
    tmp_path: Path,
    boundary: str,
):
    repo, valid = production_history(tmp_path)
    phase_paths = {
        "S..E": PRODUCTION_EVIDENCE_PATHS,
        "E..C": PRODUCTION_CLOSURE_PATHS,
        "C..W": PRODUCTION_WIKI_PATHS,
    }
    older_label, newer_label = boundary.split("..")
    added = commit_tree(
        repo,
        git(repo, "rev-parse", f"{valid[newer_label]}^{{tree}}"),
        valid[older_label],
        f"add phase destinations {boundary}",
    )
    checkout(repo, f"phase-cycle-{older_label.lower()}", added)
    (repo / phase_paths[boundary][0]).unlink()
    deleted = commit(repo, f"delete allowed phase destination {boundary}")
    endpoint = commit_tree(
        repo,
        git(repo, "rev-parse", f"{valid[newer_label]}^{{tree}}"),
        deleted,
        f"re-add phase destination {boundary}",
    )
    revised = dict(valid)
    revised[newer_label] = endpoint
    previous = endpoint
    for label in {"E": ("C", "W"), "C": ("W",), "W": ()}[newer_label]:
        previous = commit_tree(
            repo,
            git(repo, "rev-parse", f"{valid[label]}^{{tree}}"),
            previous,
            f"rebuild {label}",
        )
        revised[label] = previous
    git(repo, "update-ref", "HEAD", revised["W"])

    outcome = require_gate("validate_lifecycle", "phase edge completeness")(
        repo,
        revised["S"],
        revised["E"],
        revised["C"],
        revised["W"],
    )

    assert outcome.ok is False and any(
        boundary in finding and deleted in finding and "edge" in finding
        for finding in outcome.findings
    ), f"DEFECT [{boundary} edge]: add-delete-readd cycle passed"


def test_production_lifecycle_accepts_incremental_allowed_phase_artifacts(
    tmp_path: Path,
):
    repo = tmp_path / "incremental-production"
    repo.mkdir()
    git(repo, "init")
    for index, path in enumerate(PRODUCTION_MANDATORY_PATHS, start=1):
        write(repo, path, f"mandatory {index}\n")
    revisions = {"S": commit(repo, "source")}
    for label, paths in (
        ("E", PRODUCTION_EVIDENCE_PATHS),
        ("C", PRODUCTION_CLOSURE_PATHS),
        ("W", PRODUCTION_WIKI_PATHS),
    ):
        for index, path in enumerate(paths, start=1):
            write(repo, path, f"incremental {label} {index}\n")
            revisions[label] = commit(repo, f"incremental {label} {index}")

    outcome = require_gate("validate_lifecycle", "incremental phase history")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
    )

    assert outcome.ok is True, outcome.findings


def test_lifecycle_reports_bind_exact_fixed_git_identity_on_success_and_failure(
    tmp_path: Path,
):
    repo, revisions = history(tmp_path)
    validate = require_gate("validate_lifecycle", "lifecycle Git provenance")
    successful = validate(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )
    failed = validate(
        repo,
        "0" * 40,
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )
    expected_hash = hashlib.sha256(FIXED_GIT_EXECUTABLE.read_bytes()).hexdigest()

    for label, report in (("success", successful), ("failure", failed)):
        assert getattr(report, "git_executable", None) == str(
            FIXED_GIT_EXECUTABLE
        ), f"DEFECT [lifecycle Git provenance {label}]: fixed path is absent"
        assert getattr(report, "git_executable_sha256", None) == expected_hash, (
            f"DEFECT [lifecycle Git provenance {label}]: raw executable hash is absent"
        )
        assert getattr(report, "protocol_profile", None) == (
            "synthetic-test-fixture-v1"
        )
        if label == "success":
            assert getattr(report, "head_revision", None) == revisions["W"]
        assert set(report.to_dict()) == {
            "ok",
            "errors",
            "revisions",
            "changes",
            "protocol_profile",
            "head_revision",
            "git_executable",
            "git_executable_sha256",
        }, f"DEFECT [lifecycle report shape {label}]: report is not exact and closed"


def test_lifecycle_rejects_fixed_git_identity_change_after_m0(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    repo, revisions = history(tmp_path)
    loaded = gate_module()
    assert loaded is not None
    real_identity = loaded._fixed_git_snapshot()
    calls = 0

    def drifting_identity() -> dict[str, object]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return real_identity
        return {**real_identity, "sha256": "f" * 64}

    monkeypatch.setattr(loaded, "_fixed_git_snapshot", drifting_identity)
    report = loaded.validate_lifecycle(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )

    assert report.ok is False
    assert any("Git" in error and "changed" in error for error in report.errors)


def test_lifecycle_rejects_byte_identical_git_filesystem_identity_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    repo, revisions = history(tmp_path)
    loaded = gate_module()
    assert loaded is not None
    real_snapshot = loaded._fixed_git_snapshot()
    calls = 0

    def byte_identical_replacement() -> dict[str, object]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return real_snapshot
        changed_identity = list(real_snapshot["filesystem_identity"])
        changed_identity[1] += 1
        return {**real_snapshot, "filesystem_identity": changed_identity}

    monkeypatch.setattr(
        loaded,
        "_fixed_git_snapshot",
        byte_identical_replacement,
    )
    report = loaded.validate_lifecycle(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )

    assert report.ok is False
    assert report.git_executable_sha256 == real_snapshot["sha256"]
    assert any("Git" in error and "changed" in error for error in report.errors)


@pytest.mark.parametrize("entrypoint", ["lifecycle", "publication"])
def test_gate_rejects_head_advance_after_initial_head_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    entrypoint: str,
):
    repo, revisions = history(tmp_path)
    loaded = gate_module()
    assert loaded is not None
    real_resolve_head = loaded._resolve_head_commit
    calls = 0

    def resolve_head_then_advance(root: Path) -> str:
        nonlocal calls
        resolved = real_resolve_head(root)
        calls += 1
        if calls == 1:
            write(repo, "docs/unprotected-tip-advance.txt", "advanced during gate\n")
            commit(repo, "advance HEAD during closing metadata check")
        return resolved

    monkeypatch.setattr(
        loaded,
        "_resolve_head_commit",
        resolve_head_then_advance,
    )
    if entrypoint == "lifecycle":
        report = loaded.validate_lifecycle(
            repo,
            revisions["S"],
            revisions["E"],
            revisions["C"],
            revisions["W"],
            test_fixture=True,
        )
    else:
        report = loaded.verify_publication_identity(
            repo,
            revisions["W"],
            revisions["W"],
            test_fixture=True,
        )

    assert calls == 2
    assert report.ok is False, (
        "DEFECT [HEAD TOCTOU]: a gate must not return success for the stale tip "
        f"captured before {entrypoint} validation"
    )
    assert any("HEAD" in error and "changed" in error for error in report.errors)


@pytest.mark.parametrize(
    "boundary, forbidden",
    [
        ("S..E", "manuscripts/gauge_vfe_rg/main.tex"),
        ("S..E", "manuscripts/references.bib"),
        ("E..C", "docs/reviews/adversarial.md"),
        ("E..C", "docs/derivations/closure.json"),
        ("C..W", "docs/derivations/release.json"),
    ],
)
def test_gate_rejects_forbidden_change_on_the_exact_monotone_boundary(tmp_path: Path, boundary: str, forbidden: str):
    repo, valid = history(tmp_path)
    revised = dict(valid)
    if boundary == "S..E":
        checkout(repo, "bad-evidence", valid["S"])
        write(repo, forbidden, "forbidden\n")
        revised["E"] = commit(repo, "forbidden evidence")
        checkout(repo, "bad-closure", revised["E"])
        write(repo, "docs/derivations/closure-attestation.json", "still monotone\n")
        revised["C"] = commit(repo, "closure after bad evidence")
        checkout(repo, "bad-wiki", revised["C"])
        write(repo, "index.md", "wiki after bad evidence\n")
        revised["W"] = commit(repo, "wiki after bad evidence")
    elif boundary == "E..C":
        checkout(repo, "bad-closure", valid["E"])
        write(repo, forbidden, "forbidden\n")
        revised["C"] = commit(repo, "forbidden closure")
        checkout(repo, "bad-wiki", revised["C"])
        write(repo, "index.md", "wiki after bad closure\n")
        revised["W"] = commit(repo, "wiki after bad closure")
    else:
        checkout(repo, "bad-wiki", valid["C"])
        write(repo, forbidden, "forbidden\n")
        revised["W"] = commit(repo, "forbidden wiki")
    outcome = require_gate("validate_lifecycle", f"forbidden {boundary} {forbidden}")(
        repo,
        revised["S"],
        revised["E"],
        revised["C"],
        revised["W"],
        test_fixture=True,
    )
    assert getattr(outcome, "ok", None) is False, f"DEFECT [forbidden {boundary}]: gate accepted {forbidden}"


def test_gate_parses_exact_nul_statuses_and_utf8_paths_without_lossy_decoding():
    raw = (
        b"A\x00sources/manuscripts/sp ace-\xe2\x9c\x93.md\x00"
        b"M\x00manuscripts/gauge_vfe_rg/line\nbreak.tex\x00"
        b"D\x00docs/old\tname.md\x00"
        b"R100\x00wiki/concepts/Old Name.md\x00wiki/concepts/New Name.md\x00"
        b"C75\x00docs/source.json\x00docs/copied.json\x00"
    )
    entries = require_gate("parse_name_status_z", "NUL-safe diff parser")(raw)
    observed = tuple((entry.status, entry.paths) for entry in entries)
    assert observed == (
        ("A", ("sources/manuscripts/sp ace-\u2713.md",)),
        ("M", ("manuscripts/gauge_vfe_rg/line\nbreak.tex",)),
        ("D", ("docs/old\tname.md",)),
        ("R100", ("wiki/concepts/Old Name.md", "wiki/concepts/New Name.md")),
        ("C75", ("docs/source.json", "docs/copied.json")),
    ), "DEFECT [NUL-safe parser]: status/path tuples changed or UTF-8 was decoded lossily"


@pytest.mark.parametrize("kind", ["divergent", "nonmonotone"])
def test_gate_rejects_individually_valid_but_nonancestral_revision_tuples(tmp_path: Path, kind: str):
    repo, revisions = history(tmp_path)
    if kind == "divergent":
        checkout(repo, "parallel-evidence", revisions["E"])
        divergent_e = empty_commit(repo, "parallel evidence with identical tree")
        candidate = (revisions["S"], divergent_e, revisions["C"], revisions["W"])
    else:
        checkout(repo, "later-closure", revisions["C"])
        later_c = empty_commit(repo, "later closure with identical tree")
        candidate = (revisions["S"], revisions["E"], later_c, revisions["C"])
    outcome = require_gate("validate_lifecycle", f"{kind} ancestry")(
        repo, *candidate, test_fixture=True
    )
    assert getattr(outcome, "ok", None) is False, f"DEFECT [{kind} ancestry]: gate accepted a revision tuple that is not S -> E -> C -> W"


def test_gate_rejects_invalid_revision(tmp_path: Path):
    repo, revisions = history(tmp_path)
    invalid = require_gate("validate_lifecycle", "invalid revision")(
        repo,
        "0" * 40,
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )
    assert getattr(invalid, "ok", None) is False, "DEFECT [invalid revision]: gate accepted nonexistent revision"


def test_publication_identity_accepts_unrelated_integration_change(tmp_path: Path):
    repo, revisions = history(tmp_path)
    checkout(repo, "publication-integration", revisions["W"])
    write(repo, "docs/unrelated/remote-note.md", "unrelated integration\n")
    publication = commit(repo, "unrelated integration")
    identity = require_gate(
        "verify_publication_identity", "positive publication byte identity"
    )(repo, revisions["W"], publication, test_fixture=True)
    assert getattr(identity, "ok", None) is True, "DEFECT [publication identity]: unrelated integration was rejected despite preserving every protected byte"


@pytest.mark.parametrize(
    "protected_path",
    [
        "manuscripts/gauge_vfe_rg/main.tex",
        "manuscripts/gauge_vfe_rg/verification/current-results.json",
        "docs/derivations/closure-attestation.json",
        "docs/derivations/release.json",
    ],
)
def test_publication_identity_rejects_each_protected_byte_drift(tmp_path: Path, protected_path: str):
    repo, revisions = history(tmp_path)
    checkout(repo, "publication-drift", revisions["W"])
    write(repo, protected_path, "changed after W\n")
    publication = commit(repo, "publication drift")
    identity = require_gate("verify_publication_identity", "publication byte identity")(
        repo, revisions["W"], publication, test_fixture=True
    )
    assert getattr(identity, "ok", None) is False, f"DEFECT [publication identity]: gate accepted drift in protected path {protected_path}"


def test_gate_ignores_repository_local_commit_replacement_overlays(tmp_path: Path):
    repo, revisions = history(tmp_path)
    git(repo, "replace", revisions["W"], revisions["S"])
    outcome = require_gate("validate_lifecycle", "replacement-object isolation")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )
    assert getattr(outcome, "ok", None) is True, (
        "DEFECT [replacement-object isolation]: local git-replace state changed "
        "the validated committed lifecycle"
    )


def test_gate_rejects_annotated_tag_object_id_even_when_it_peels_to_w(tmp_path: Path):
    repo, revisions = history(tmp_path)
    git(
        repo,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "tag",
        "-a",
        "annotated-w",
        "-m",
        "annotated W",
        revisions["W"],
    )
    tag_object_id = git(repo, "rev-parse", "refs/tags/annotated-w")
    outcome = require_gate("validate_lifecycle", "commit-object-only revisions")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        tag_object_id,
        test_fixture=True,
    )
    assert getattr(outcome, "ok", None) is False, (
        "DEFECT [commit-object-only revisions]: annotated-tag object ID was "
        "accepted as a caller revision"
    )


def test_every_gate_git_read_disables_replacements_and_uses_literal_pathspecs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, revisions = history(tmp_path)
    loaded = gate_module()
    assert loaded is not None
    real_run = subprocess.run
    observed_argv: list[tuple[str, ...]] = []
    observed_envs: list[dict[str, str]] = []

    def recording_run(argv, *args, **kwargs):
        observed_argv.append(tuple(argv))
        observed_envs.append(dict(kwargs.get("env", {})))
        return real_run(argv, *args, **kwargs)

    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(repo))
    monkeypatch.setattr(loaded.subprocess, "run", recording_run)
    outcome = loaded.validate_lifecycle(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )
    assert outcome.ok is True
    assert observed_argv and all(
        argv[:3]
        == (
            str(FIXED_GIT_EXECUTABLE),
            "--no-replace-objects",
            "--literal-pathspecs",
        )
        for argv in observed_argv
    ), (
        "DEFECT [literal immutable Git reads]: at least one gate Git read "
        "honored replacements or nonliteral pathspec magic"
    )
    assert observed_envs and all(
        not any(key.casefold().startswith("git_") for key in environment)
        for environment in observed_envs
    ), "DEFECT [controlled Git metadata]: a gate Git read inherited caller GIT_*"


def test_production_gate_accepts_complete_fixed_envelope_and_exact_wiki_delta(
    tmp_path: Path,
):
    repo, revisions = production_history(tmp_path)
    outcome = require_gate("validate_lifecycle", "complete production lifecycle")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
    )
    assert getattr(outcome, "ok", None) is True, (
        "DEFECT [complete production lifecycle]: complete production fixture was rejected"
    )


def test_fixture_policy_rejects_production_marker_in_current_head(
    tmp_path: Path,
):
    repo, revisions = history(tmp_path)
    checkout(repo, "production-head", revisions["W"])
    write(repo, PRODUCTION_TASK_PLAN, "current HEAD production marker\n")
    commit(repo, "production current HEAD")
    outcome = require_gate("validate_lifecycle", "HEAD-independent profile")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )
    assert getattr(outcome, "ok", None) is False and any(
        "test fixture" in finding for finding in getattr(outcome, "findings", ())
    ), (
        "DEFECT [fixture policy]: a production marker in current HEAD was "
        "accepted under the explicit synthetic policy"
    )


def test_publication_production_policy_rejects_mandatory_envelope_removal(
    tmp_path: Path,
):
    repo, revisions = production_history(tmp_path)
    checkout(repo, "synthetic-publication", revisions["W"])
    for path in (
        PRODUCTION_TASK_PLAN,
        "manuscripts/gauge_vfe_rg/SPEC.md",
        "manuscripts/gauge_vfe_rg/verification/claims.json",
    ):
        (repo / path).unlink()
    publication = commit(repo, "remove production profile markers")
    outcome = require_gate("verify_publication_identity", "W/P profile consistency")(
        repo, revisions["W"], publication
    )
    assert getattr(outcome, "ok", None) is False and any(
        "mandatory" in finding for finding in getattr(outcome, "findings", ())
    ), "DEFECT [production policy]: publication mandatory-envelope drift was not diagnosed"


@pytest.mark.parametrize(
    "missing_path",
    [
        "manuscripts/gauge_vfe_rg/main.tex",
        "manuscripts/gauge_vfe_rg/verification/build_audit.py",
        "manuscripts/gauge_vfe_rg/verification/build_bootstrap_reference.ps1.txt",
        "manuscripts/gauge_vfe_rg/verification/build_bootstrap_transport.txt",
        "manuscripts/gauge_vfe_rg/verification/tests/test_build_bootstrap.py",
        "manuscripts/scientific_report.sty",
    ],
)
def test_production_gate_rejects_missing_fixed_mandatory_envelope_path(
    tmp_path: Path, missing_path: str
):
    repo, revisions = production_history(tmp_path, missing_mandatory=missing_path)
    outcome = require_gate("validate_lifecycle", "mandatory production envelope")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
    )
    assert getattr(outcome, "ok", None) is False and any(
        "mandatory" in finding and missing_path in finding
        for finding in getattr(outcome, "findings", ())
    ), (
        f"DEFECT [mandatory production envelope]: missing path was accepted: {missing_path}"
    )


@pytest.mark.parametrize(
    "new_path",
    [
        "manuscripts/gauge_vfe_rg/UNDECLARED.TEX",
        "manuscripts/gauge_vfe_rg/verification/unknown-governed.bin",
    ],
)
def test_publication_rejects_unknown_or_uppercase_addition_anywhere_under_manuscript_root(
    tmp_path: Path, new_path: str
):
    repo, revisions = history(tmp_path)
    checkout(repo, "publication-unknown-governed", revisions["W"])
    write(repo, new_path, "unknown governed addition\n")
    publication = commit(repo, "unknown governed addition")
    outcome = require_gate(
        "verify_publication_identity", "whole manuscript root protection"
    )(repo, revisions["W"], publication, test_fixture=True)
    assert getattr(outcome, "ok", None) is False, (
        "DEFECT [whole manuscript root protection]: publication accepted "
        f"new protected path {new_path}"
    )


def test_publication_rejects_task_plan_byte_drift(tmp_path: Path):
    repo, revisions = production_history(tmp_path)
    checkout(repo, "publication-task-plan-drift", revisions["W"])
    write(repo, PRODUCTION_TASK_PLAN, "changed after W\n")
    publication = commit(repo, "task plan drift")
    outcome = require_gate("verify_publication_identity", "all task path identity")(
        repo, revisions["W"], publication
    )
    assert getattr(outcome, "ok", None) is False, (
        "DEFECT [all task path identity]: publication accepted task-plan byte drift"
    )


def test_production_gate_requires_exactly_all_seven_wiki_paths_to_change(
    tmp_path: Path,
):
    repo, revisions = production_history(
        tmp_path,
        preseed_wiki=True,
        changed_wiki_paths=PRODUCTION_WIKI_PATHS[:-1],
    )
    outcome = require_gate("validate_lifecycle", "exact production C/W delta")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
    )
    assert getattr(outcome, "ok", None) is False and any(
        "exact" in finding and "seven" in finding
        for finding in getattr(outcome, "findings", ())
    ), "DEFECT [exact production C/W delta]: six-path wiki revision was accepted"


@pytest.mark.parametrize("status", ["R00", "R01", "C000", "C075"])
def test_parser_rejects_noncanonical_leading_zero_rename_copy_score(status: str):
    raw = status.encode("ascii") + b"\0old\0new\0"
    parser = require_gate("parse_name_status_z", "canonical R/C score parser")
    with pytest.raises(ValueError, match="status"):
        parser(raw)


def test_absent_optional_git_metadata_is_the_clean_positive_state(tmp_path: Path):
    repo, _revisions = history(tmp_path)
    loaded = gate_module()

    loaded._require_controlled_git_metadata(repo)

    for relative in loaded._CONTROLLED_GIT_METADATA_PATHS:
        assert not (repo / ".git" / relative).exists()


def test_stable_metadata_read_rejects_disappearance_after_initial_lstat(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = gate_module()
    target = tmp_path / "observed-metadata"
    target.write_bytes(b"")
    real_open = Path.open
    removed = False

    def remove_after_initial_observation(path: Path, *args, **kwargs):
        nonlocal removed
        if path == target and not removed:
            target.unlink()
            removed = True
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", remove_after_initial_observation)

    with pytest.raises(loaded.LifecycleGateError, match="cannot read"):
        loaded._stable_regular_file_bytes(target, "observed metadata")

    assert removed is True


@pytest.mark.parametrize(
    "override",
    [
        "caller-environment",
        "info/grafts",
        "shallow",
        "objects/info/alternates",
        "objects/info/http-alternates",
    ],
)
def test_gate_sanitizes_caller_git_environment_and_rejects_git_metadata_overrides(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, override: str
):
    repo, revisions = history(tmp_path)
    gate = require_gate("validate_lifecycle", "controlled Git metadata")
    if override == "caller-environment":
        attacker = tmp_path / "attacker"
        attacker.mkdir()
        git(attacker, "init")
        write(attacker, "attacker.txt")
        commit(attacker, "attacker")
        monkeypatch.setenv("GIT_DIR", str(attacker / ".git"))
        monkeypatch.setenv("GIT_WORK_TREE", str(attacker))
        monkeypatch.setenv("GIT_OBJECT_DIRECTORY", str(attacker / ".git" / "objects"))
        outcome = gate(
            repo,
            revisions["S"],
            revisions["E"],
            revisions["C"],
            revisions["W"],
            test_fixture=True,
        )
        assert outcome.ok is True, (
            "DEFECT [controlled Git metadata]: caller GIT_* variables changed "
            "the repository read context"
        )
        return

    metadata_path = repo / ".git" / override
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    if override == "info/grafts":
        payload = f'{revisions["W"]} {revisions["S"]}\n'
    elif override == "shallow":
        payload = f'{revisions["S"]}\n'
    else:
        alternate = tmp_path / "alternate"
        alternate.mkdir()
        git(alternate, "init")
        write(alternate, "alternate.txt")
        commit(alternate, "alternate")
        payload = f'{(alternate / ".git" / "objects").as_posix()}\n'
    metadata_path.write_text(payload, encoding="utf-8")
    outcome = gate(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )
    assert outcome.ok is False and any(
        override in finding for finding in outcome.findings
    ), f"DEFECT [controlled Git metadata]: nonempty {override} was not rejected"


def test_lifecycle_git_postflight_rejects_boundary_visible_metadata_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    repo, _revisions = history(tmp_path)
    loaded = gate_module()
    real_run = loaded.subprocess.run
    metadata = repo / ".git/info/grafts"
    mutated = False

    def mutate_before_subprocess_returns(command, *args, **kwargs):
        nonlocal mutated
        completed = real_run(command, *args, **kwargs)
        if not mutated:
            metadata.parent.mkdir(parents=True, exist_ok=True)
            metadata.write_bytes(b"forbidden\n")
            mutated = True
        return completed

    monkeypatch.setattr(loaded.subprocess, "run", mutate_before_subprocess_returns)
    try:
        with pytest.raises(loaded.LifecycleGateError, match="nonempty"):
            loaded._run_git(repo, ["rev-parse", "HEAD"])
    finally:
        metadata.unlink(missing_ok=True)

    assert mutated is True


def test_lifecycle_git_launch_exception_still_executes_metadata_postflight(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    repo, _revisions = history(tmp_path)
    loaded = gate_module()
    real_metadata_check = loaded._require_controlled_git_metadata
    metadata_checks = 0

    def counting_metadata_check(repo_root: Path, **kwargs):
        nonlocal metadata_checks
        metadata_checks += 1
        return real_metadata_check(repo_root, **kwargs)

    def launch_failure(*_args, **_kwargs):
        raise OSError("synthetic Git launch failure")

    monkeypatch.setattr(
        loaded,
        "_require_controlled_git_metadata",
        counting_metadata_check,
    )
    monkeypatch.setattr(loaded.subprocess, "run", launch_failure)

    with pytest.raises(OSError, match="synthetic Git launch failure"):
        loaded._run_git(repo, ["rev-parse", "HEAD"])

    assert metadata_checks == 3


def test_lifecycle_git_launch_exception_still_detects_executable_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    repo, _revisions = history(tmp_path)
    loaded = gate_module()
    real_snapshot = loaded._fixed_git_snapshot
    snapshot_calls = 0

    def drifting_snapshot():
        nonlocal snapshot_calls
        snapshot = real_snapshot()
        snapshot_calls += 1
        if snapshot_calls > 1:
            snapshot = {**snapshot, "sha256": "f" * 64}
        return snapshot

    def launch_failure(*_args, **_kwargs):
        raise OSError("synthetic Git launch failure")

    monkeypatch.setattr(loaded, "_fixed_git_snapshot", drifting_snapshot)
    monkeypatch.setattr(loaded.subprocess, "run", launch_failure)

    with pytest.raises(OSError, match="synthetic Git launch failure") as caught:
        loaded._run_git(repo, ["rev-parse", "HEAD"])

    assert snapshot_calls >= 2
    assert isinstance(caught.value.__cause__, loaded.LifecycleGateError)
    assert "changed across one subprocess" in str(caught.value.__cause__)


def test_gate_ignores_caller_path_when_selecting_fixed_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, revisions = history(tmp_path)
    shadow = tmp_path / "shadow-bin"
    shadow.mkdir()
    shutil.copy2(Path(os.environ["SystemRoot"]) / "System32/where.exe", shadow / "git.exe")
    monkeypatch.setenv("PATH", f"{shadow}{os.pathsep}{os.environ.get('PATH', '')}")

    outcome = require_gate("validate_lifecycle", "fixed Git executable")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )

    assert outcome.ok is True, (
        "DEFECT [fixed Git executable]: caller PATH replaced the Git identity used "
        f"by the gate: {outcome.findings}"
    )


def test_gate_rejects_empty_alternates_through_reparse_parent(tmp_path: Path):
    repo, revisions = history(tmp_path)
    info_path = repo / ".git/objects/info"
    external_info = tmp_path / "external-object-info"
    external_info.mkdir()
    (external_info / "alternates").touch()
    if info_path.exists():
        shutil.rmtree(info_path)
    completed = subprocess.run(
        [
            os.environ.get("COMSPEC", r"C:\Windows\System32\cmd.exe"),
            "/d",
            "/c",
            "mklink",
            "/J",
            str(info_path),
            str(external_info),
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout

    try:
        outcome = require_gate("validate_lifecycle", "reparse metadata parent")(
            repo,
            revisions["S"],
            revisions["E"],
            revisions["C"],
            revisions["W"],
            test_fixture=True,
        )
    finally:
        os.rmdir(info_path)

    assert outcome.ok is False and any(
        "reparse" in finding.lower() for finding in outcome.findings
    ), "DEFECT [reparse metadata parent]: empty alternates through a junction passed"


def test_production_is_default_and_test_fixture_policy_rejects_production_envelope(
    tmp_path: Path,
):
    synthetic_root = tmp_path / "synthetic"
    synthetic_root.mkdir()
    repo, revisions = history(synthetic_root)
    default_outcome = require_gate("validate_lifecycle", "production default")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
    )
    assert default_outcome.ok is False and any(
        "production" in finding for finding in default_outcome.findings
    ), "DEFECT [production default]: a synthetic history received production trust"

    production_root = tmp_path / "production"
    production_root.mkdir()
    production_repo, production_revisions = production_history(production_root)
    fixture_outcome = require_gate("validate_lifecycle", "test-fixture isolation")(
        production_repo,
        production_revisions["S"],
        production_revisions["E"],
        production_revisions["C"],
        production_revisions["W"],
        test_fixture=True,
    )
    assert fixture_outcome.ok is False and any(
        "test fixture" in finding for finding in fixture_outcome.findings
    ), "DEFECT [test-fixture isolation]: production envelope entered synthetic mode"


@pytest.mark.parametrize("gate_kind", ["lifecycle", "publication"])
def test_gate_requires_candidate_tip_to_be_reachable_from_current_head(
    tmp_path: Path, gate_kind: str
):
    repo, revisions = history(tmp_path)
    if gate_kind == "lifecycle":
        checkout(repo, "divergent-current-head", revisions["C"])
        write(repo, "docs/unrelated/current-head.md", "divergent current HEAD\n")
        commit(repo, "divergent current HEAD")
        outcome = require_gate("validate_lifecycle", "W reachable from HEAD")(
            repo,
            revisions["S"],
            revisions["E"],
            revisions["C"],
            revisions["W"],
            test_fixture=True,
        )
        boundary = "W..HEAD"
    else:
        checkout(repo, "publication-candidate", revisions["W"])
        write(repo, "docs/unrelated/publication.md", "publication candidate\n")
        publication = commit(repo, "publication candidate")
        checkout(repo, "divergent-current-head", revisions["W"])
        write(repo, "docs/unrelated/current-head.md", "divergent current HEAD\n")
        commit(repo, "divergent current HEAD")
        outcome = require_gate(
            "verify_publication_identity", "P reachable from HEAD"
        )(
            repo,
            revisions["W"],
            publication,
            test_fixture=True,
        )
        boundary = "P..HEAD"
    assert outcome.ok is False and any(
        boundary in finding for finding in outcome.findings
    ), f"DEFECT [current HEAD reachability]: gate accepted non-reachable {boundary}"


def test_lifecycle_rejects_protected_drift_in_descendant_head(tmp_path: Path):
    repo, revisions = production_history(tmp_path)
    write(repo, "manuscripts/gauge_vfe_rg/main.tex", "protected HEAD drift\n")
    descendant_head = commit(repo, "protected drift after W")

    outcome = require_gate("validate_lifecycle", "protected W-to-HEAD identity")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
    )

    assert outcome.ok is False and any(
        descendant_head in finding and "W..HEAD" in finding
        for finding in outcome.findings
    ), "DEFECT [protected W-to-HEAD identity]: descendant HEAD drift passed"


def test_lifecycle_rejects_protected_change_restored_before_head(tmp_path: Path):
    repo, revisions = history(tmp_path)
    protected = repo / "manuscripts/gauge_vfe_rg/verification/current-results.json"
    original = protected.read_bytes()
    protected.write_bytes(b'{"altered":true}\n')
    changed = commit(repo, "temporarily alter protected evidence")
    protected.write_bytes(original)
    restored_head = commit(repo, "restore protected evidence")

    outcome = require_gate("validate_lifecycle", "W-to-HEAD history purity")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )

    assert outcome.ok is False and any(
        changed in finding and "W..HEAD" in finding
        for finding in outcome.findings
    ), (
        "DEFECT [W-to-HEAD history purity]: protected bytes changed at "
        f"{changed}, restored at {restored_head}, and passed"
    )


@pytest.mark.parametrize("restore_before", ["P", "HEAD"])
def test_publication_rejects_protected_change_restored_within_descendant_range(
    tmp_path: Path, restore_before: str
):
    repo, revisions = history(tmp_path)
    protected = repo / "manuscripts/gauge_vfe_rg/verification/current-results.json"
    original = protected.read_bytes()
    if restore_before == "P":
        protected.write_bytes(b'{"altered-at-p1":true}\n')
        changed = commit(repo, "temporarily alter protected evidence before P")
        protected.write_bytes(original)
        publication = commit(repo, "restore protected evidence at P")
    else:
        write(repo, "docs/unrelated/publication.md", "publication candidate\n")
        publication = commit(repo, "P preserves protected evidence")
        protected.write_bytes(b'{"altered-after-p":true}\n')
        changed = commit(repo, "temporarily alter protected evidence after P")
        protected.write_bytes(original)
        commit(repo, "restore protected evidence at HEAD")

    outcome = require_gate(
        "verify_publication_identity", "publication ancestry history purity"
    )(
        repo,
        revisions["W"],
        publication,
        test_fixture=True,
    )
    expected_boundary = "W..P" if restore_before == "P" else "P..HEAD"

    assert outcome.ok is False and any(
        changed in finding and expected_boundary in finding
        for finding in outcome.findings
    ), (
        f"DEFECT [{expected_boundary} history purity]: protected change at "
        f"{changed} was hidden by a later restore"
    )


@pytest.mark.parametrize("drift", ("bytes", "type", "existence"))
@pytest.mark.parametrize("boundary", ("W..HEAD", "W..P", "P..HEAD"))
def test_post_w_and_publication_reject_deep_unrelated_protected_drift_restoration(
    tmp_path: Path,
    boundary: str,
    drift: str,
):
    repo, revisions = history(tmp_path)
    attacked, restored, protected = deep_protected_side_dag(
        repo,
        revisions["W"],
        drift,
    )
    clean_tree = git(repo, "rev-parse", f'{revisions["W"]}^{{tree}}')
    if boundary == "W..HEAD":
        head = commit_tree_with_parents(
            repo,
            clean_tree,
            (revisions["W"], restored),
            f"merge restored {drift} side-DAG after W",
        )
        git(repo, "update-ref", "HEAD", head)
        outcome = require_gate("validate_lifecycle", "complete W-to-HEAD DAG")(
            repo,
            revisions["S"],
            revisions["E"],
            revisions["C"],
            revisions["W"],
            test_fixture=True,
        )
    elif boundary == "W..P":
        publication = commit_tree_with_parents(
            repo,
            clean_tree,
            (revisions["W"], restored),
            f"publication merges restored {drift} side-DAG",
        )
        git(repo, "update-ref", "HEAD", publication)
        outcome = require_gate("verify_publication_identity", "complete W-to-P DAG")(
            repo,
            revisions["W"],
            publication,
            test_fixture=True,
        )
    else:
        publication = commit_tree(
            repo,
            clean_tree,
            revisions["W"],
            "protected-clean publication candidate",
        )
        head = commit_tree_with_parents(
            repo,
            clean_tree,
            (publication, restored),
            f"HEAD merges restored {drift} side-DAG after P",
        )
        git(repo, "update-ref", "HEAD", head)
        outcome = require_gate("verify_publication_identity", "complete P-to-HEAD DAG")(
            repo,
            revisions["W"],
            publication,
            test_fixture=True,
        )

    assert outcome.ok is False and any(
        boundary in finding
        and attacked in finding
        and protected in finding
        and "protected history violation" in finding
        for finding in outcome.findings
    ), (
        f"DEFECT [{boundary} complete DAG]: deep protected {drift} drift at "
        f"{attacked} was hidden by restoration at {restored}: {outcome.findings}"
    )


def test_post_w_accepts_unrelated_side_dag_whose_every_tree_preserves_w(
    tmp_path: Path,
):
    repo, revisions = history(tmp_path)
    checkout(repo, "W-clean-unrelated-tree", revisions["W"])
    write(repo, "docs/unrelated/side-root.md", "unprotected unrelated history\n")
    side_tree_source = commit(repo, "W-clean unrelated tree source")
    side_root = commit_tree_with_parents(
        repo,
        git(repo, "rev-parse", f"{side_tree_source}^{{tree}}"),
        (),
        "unrelated root preserving W protected identity",
    )
    head = commit_tree_with_parents(
        repo,
        git(repo, "rev-parse", f'{revisions["W"]}^{{tree}}'),
        (revisions["W"], side_root),
        "merge W-clean unrelated side DAG",
    )
    git(repo, "update-ref", "HEAD", head)

    outcome = require_gate("validate_lifecycle", "valid W-clean side DAG")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )

    assert outcome.ok is True, (
        "DEFECT [valid W-clean side DAG]: unrelated integration preserving every "
        f"protected tree was rejected: {outcome.findings}"
    )


def test_pre_w_side_branch_missing_w_protected_state_is_rejected_when_imported(
    tmp_path: Path,
):
    repo, revisions = history(tmp_path)
    checkout(repo, "pre-w-side", revisions["S"])
    write(repo, "docs/unrelated/pre-w-side.md", "unrelated pre-W branch\n")
    side_commit = commit(repo, "unrelated pre-W side branch")
    checkout(repo, "post-w-merge", revisions["W"])
    git(
        repo,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "merge",
        "--no-ff",
        "--no-edit",
        side_commit,
    )

    outcome = require_gate("validate_lifecycle", "pre-W side-branch merge")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
        test_fixture=True,
    )

    assert outcome.ok is False and any(
        side_commit in finding and "W..HEAD" in finding
        for finding in outcome.findings
    ), (
        "DEFECT [pre-W side-branch import]: a newly imported commit missing W's "
        f"protected state passed: {outcome.findings}"
    )


@pytest.mark.parametrize(
    "scenario",
    [
        *(f"{boundary}:{status}" for boundary in ("S..E", "E..C", "C..W") for status in ("D", "R", "C", "T")),
        "S..E:missing-envelope",
        "E..C:missing-envelope",
    ],
)
def test_production_phase_boundaries_require_a_m_destinations_and_e_c_envelopes(
    tmp_path: Path, scenario: str
):
    boundary, status = scenario.split(":", 1)
    if status == "missing-envelope":
        missing = (
            PRODUCTION_EVIDENCE_PATHS[-1]
            if boundary == "S..E"
            else PRODUCTION_CLOSURE_PATHS[-1]
        )
        options = (
            {"missing_evidence": missing}
            if boundary == "S..E"
            else {"missing_closure": missing}
        )
        repo, revisions = production_history(tmp_path, **options)
    else:
        missing = None
        repo, revisions = production_history_with_status(tmp_path, boundary, status)
    outcome = require_gate("validate_lifecycle", "production phase destinations")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
    )
    if status == "missing-envelope":
        assert outcome.ok is False and any(
            "destination envelope" in finding and missing in finding
            for finding in outcome.findings
        ), f"DEFECT [phase destination envelope]: {boundary} accepted missing {missing}"
    else:
        assert outcome.ok is False and any(
            boundary in finding
            and "one-path A/M" in finding
            and f"status {status}" in finding
            for finding in outcome.findings
        ), f"DEFECT [phase status]: {boundary} accepted or misdiagnosed {status}"


def test_production_exact_seven_uses_only_a_m_destination_paths(tmp_path: Path):
    repo, revisions = production_history_with_status(tmp_path, "C..W", "C")
    outcome = require_gate("validate_lifecycle", "C/W destination set")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
    )
    assert outcome.ok is False and any(
        "exactly all seven" in finding
        and PRODUCTION_WIKI_PATHS[0] in finding
        and "missing" in finding
        for finding in outcome.findings
    ), "DEFECT [C/W destination set]: copy source path counted as a changed wiki destination"


def test_publication_casefolds_governed_roots_and_rejects_noncanonical_casing(
    tmp_path: Path,
):
    repo, revisions = production_history(tmp_path)
    checkout(repo, "noncanonical-w", revisions["W"])
    blob_oid = git(
        repo,
        "rev-parse",
        f'{revisions["W"]}:manuscripts/gauge_vfe_rg/main.tex',
    )
    noncanonical = "Manuscripts/gauge_vfe_rg/unchanged.bin"
    git(
        repo,
        "update-index",
        "--add",
        "--cacheinfo",
        f"100644,{blob_oid},{noncanonical}",
    )
    noncanonical_w = commit_index(repo, "noncanonical governed path")
    publication = empty_commit(repo, "publication preserves noncanonical path")
    outcome = require_gate("verify_publication_identity", "casefold protection")(
        repo, noncanonical_w, publication
    )
    assert outcome.ok is False and any(
        "noncanonical casing" in finding and noncanonical in finding
        for finding in outcome.findings
    ), "DEFECT [casefold protection]: noncanonical protected namespace was ignored"


def test_production_mandatory_endpoints_include_plan_and_design_controls(
    tmp_path: Path,
):
    repo, revisions = production_history(
        tmp_path, missing_mandatory=PRODUCTION_TASK_DESIGN
    )
    outcome = require_gate("validate_lifecycle", "task control envelope")(
        repo,
        revisions["S"],
        revisions["E"],
        revisions["C"],
        revisions["W"],
    )
    assert outcome.ok is False and any(
        "mandatory" in finding and PRODUCTION_TASK_DESIGN in finding
        for finding in outcome.findings
    ), "DEFECT [task controls]: production endpoints accepted a missing design contract"
