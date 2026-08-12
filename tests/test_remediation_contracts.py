"""Frozen contracts for the scientific-integrity remediation program."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


AUDIT_DISPOSITION_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "verification"
    / "remediation"
    / "audit-disposition-v1.json"
)
COMPATIBILITY_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "verification"
    / "remediation"
    / "compatibility-inventory-v1.json"
)
STATUS_FAILURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "verification"
    / "remediation"
    / "status-failure-contract-v1.json"
)
HISTORICAL_BUNDLES_PATH = (
    ROOT
    / "docs"
    / "verification"
    / "remediation"
    / "historical-fixed-ray-bundles-v1.json"
)

README_PATH = ROOT / Path('docs/verification/remediation/README.md')
REMEDIATION_EVIDENCE_SCHEMA_PATH = (
    ROOT / 'docs/verification/remediation/remediation-evidence-v1.schema.json'
)
EXPECTED_REMEDIATION_WAVES = [
    'wave-0',
    'wave-a',
    'wave-b',
    'wave-c',
    'wave-d0',
    'wave-d1',
    'wave-e',
]
EXPECTED_EVIDENCE_KINDS = [
    'command',
    'junit',
    'environment',
    'dependency',
    'plan_binding',
    'privacy_transform',
    'reproduced_source',
    'review',
    'adjudicator',
    'domain',
]
WAVE0_DEPENDENCY_PATHS = [
    'pyproject.toml',
    'environments/cuda-rtx5090-cu128.lock.txt',
    'docs/verification/remediation/verification-contract-v1.json',
]
WAVE0_POLICY_SCHEMA = 'wave-0-source-config-theory-tools-tests-v1'
WAVE0_SELECTION_RULES = [
    'prefix:src/',
    'prefix:tests/',
    'prefix:Theory/',
    'prefix:tools/',
    'top_level_suffix:.py',
    'exact:pyproject.toml',
    'exact:.gitignore',
    'exact:.gitattributes',
    'exact:environments/cuda-rtx5090-cu128.lock.txt',
    'exact:docs/audits/2026-08-11-post-fixed-ray-deep-audit.md',
    (
        'exact:docs/superpowers/specs/'
        '2026-08-11-scientific-integrity-remediation-program-design.md'
    ),
    (
        'exact:docs/superpowers/plans/'
        '2026-08-11-scientific-integrity-remediation-wave-0.md'
    ),
    'exact:docs/verification/remediation/verification-contract-v1.json',
    'prefix:docs/verification/remediation/',
]
WAVE0_EXCLUSION_RULES = [
    'prefix:docs/verification/evidence/',
    'prefix:verification-evidence/',
    'prefix:.verification/',
    'prefix:.pytest_cache/',
    'prefix:.pytest-',
]


EXPECTED_HISTORICAL_BUNDLES = {
    "gaussian-confirmatory-fcb2c49": {
        "historical_git_revision": "fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05",
        "file_count": 10,
        "path_prefix": (
            "docs/verification/evidence/"
            "2026-08-10-gaussian-confirmatory-fcb2c49/"
        ),
    },
    "fixed-model-attraction-diagnostic": {
        "historical_git_revision": "039df35daa30a49e90f178edde7bfc999a7ee629",
        "file_count": 9,
        "path_prefix": (
            "docs/verification/evidence/"
            "2026-08-10-fixed-model-attraction-diagnostic/"
        ),
    },
}
EXPECTED_HISTORICAL_LIMITATION = (
    "Observed historical bytes support compatibility and reproduction only; they do not "
    "acquire manifest-v2 self-integrity or current scientific promotion."
)

EXPECTED_OWNERS = {
    "AUD-01": "B", "AUD-02": "B", "AUD-03": "A", "AUD-04": "B",
    "AUD-05": "B", "AUD-06": "C", "AUD-07": "C", "AUD-08": "C",
    "AUD-09": "C", "AUD-10": "B", "AUD-11": "B", "AUD-12": "B",
    "AUD-13": "A", "AUD-14": "A", "AUD-15": "A", "AUD-16": "A",
    "AUD-17": "A", "AUD-18": "A", "AUD-19": "C", "AUD-20": "E",
    "AUD-21": "D", "AUD-22": "D",
}

EXPECTED_PROGRAM_DESIGN_REVISION = "c43a7c50675cf63b60f7b6cbea9664b638cd4c4e"
EXPECTED_AUDIT_BASELINE_REVISION = "aedc6621a4e4f1c725a54f8b287aac425ef833d8"
EXPECTED_AUDIT_IDS = tuple(EXPECTED_OWNERS)
# This catches any literal item-value change, including the non-owner fields.
EXPECTED_ITEMS_CANONICAL_SHA256 = "b2e2587cb8a656a8338fb6937428f895a1f9f28650eccb47f16b9806cb80884c"

REQUIRED_SURFACE_IDS = {
    "a-probability-measure", "a-finite-measure", "a-markov-kernel",
    "a-kl-divergence", "a-information-point", "a-recovery-diagnostics",
    "a-recovery-function", "a-matrix-domain-policy", "a-conditioning-assessment",
    "a-quotient-assessment", "a-fisher-channel-witness", "a-assemble-precision",
    "a-assess-spectral-psd", "a-assess-spectral-spd",
    "a-assess-spectral-quotient", "a-assess-symmetric-matrix",
    "a-assess-information-recovery", "a-exact-fisher-witness-factory",
    "b-metric-record", "b-finite-metric-alias", "b-gaussian-metric-alias",
    "b-metric-comparator", "b-load-metric-record", "b-premise-assessment",
    "b-premise-helper", "b-rng-streams", "b-output-root",
    "b-prepared-run-bundle", "b-run-store", "b-npz-array-input",
    "b-run-payloads", "b-prepared-artifact", "b-verified-run-bundle",
    "b-legacy-observed-bundle", "b-prepare-run", "b-publish-run",
    "b-load-run", "b-render-run", "b-load-verified-run",
    "b-verify-legacy-run", "b-figure-cache-identity", "b-run-manifest-v1",
    "b-run-manifest-v2", "b-legacy-observation", "b-figure-generation",
    "b-figure-pointer", "b-figure-journal", "b-launch-finite",
    "b-launch-network", "b-launch-attention", "b-launch-categorical",
    "b-launch-counterexample", "b-launch-information", "b-launch-scale",
    "b-launch-theory", "b-launch-holonomy", "b-launch-gaussian",
    "b-launch-fixed-diagnostic", "b-launch-fixed-ray", "b-launch-figures",
    "c-fixed-ray-system", "c-preregistered-system", "c-execution-identity",
    "c-device-index", "c-deterministic", "c-allow-tf32", "c-worker-manifest",
    "c-worker-result", "c-worker-runtime-binding-v3", "c-worker-request-v3",
    "c-worker-response-v3", "c-legacy-worker-observation", "c-sentinel",
    "c-confirmatory", "c-fixed-run", "c-frozen-matrix-policy",
    "c-identity-validator", "c-run-manifest-v3", "c-prepare-fixed-run",
    "c-load-fixed-run", "c-legacy-fixed-observation", "c-fixed-schema-idle-gate",
    "c-fixed-schema-confirmatory-gate", "c-fixed-schema-sentinel",
    "c-fixed-schema-worker-exchange-index", "c-fixed-schema-confirmatory-job",
    "c-fixed-schema-primary-execution", "c-fixed-schema-holdout-execution",
    "c-fixed-schema-confirmatory-execution", "c-fixed-schema-confirmatory-endpoints",
    "c-fixed-schema-job-table", "c-fixed-schema-pilot-endpoints",
    "c-retained-order", "c-collect-diagnostics", "d-timing-observation",
    "d-clock", "d-perf-counter-clock", "d-timing-span", "d-cpu-profile",
    "d-worker-timing",
}

EXPECTED_MIGRATIONS = {
    "candidate_only_producer",
    "canonical_root_resolution",
    "factory_only_status_derivation",
    "immutable_generation_publication",
    "immutable_snapshot_semantics",
    "new_measurement_surface",
    "new_public_assessment",
    "new_schema_version_legacy_read_only",
    "new_strict_public_path",
    "preserve_signature_stricter_invariant",
    "reject_previously_accepted_unsupported_value",
    "required_execution_identity",
    "required_keyword_domain_policy",
    "strict_version_dispatch",
    "transport_and_validate_previously_inert_field",
}

REQUIRED_EFFECT_ENTRY_POINTS = {
    "ProbabilityMeasure.__init__", "FiniteMeasure.__init__", "MarkovKernel.__init__",
    "InformationPoint.__init__", "ExperimentConfig.from_dicts",
    "MetricRecord.__init__", "metric_factories", "RngStreams.create",
    "assemble_precision", "recovery_diagnostics", "FixedRaySystem.__init__",
    "validate_fixed_ray_execution_identity", "resolve_output_root",
    "prepare_run_bundle", "publish_run_bundle", "load_run_bundle", "render_run",
    "run_finite_experiment", "run_multiagent_network_experiment",
    "run_attention_experiment", "run_categorical_dqm_experiment",
    "run_counterexample_experiment", "run_information_history_experiment",
    "run_scale_cocycle_experiment", "run_theory_oracle_experiment",
    "run_gauge_holonomy_experiment", "run_gaussian_experiment",
    "run_gaussian_fixed_ray_diagnostic", "run_fixed_ray_experiment",
    "run_cuda_sentinel", "publish_confirmatory_experiment", "run_worker_job",
    "run_remediation_performance_profile",
}

EXPECTED_STATES = {
    "theorem_status": ["ESTABLISHED", "HYPOTHESIS", "CONJECTURE", "NUMERICAL", "OPEN"],
    "producer_verification_state": ["CANDIDATE"],
    "assessment_decision": ["fail", "inconclusive", "pass"],
    "run_status": ["incomplete", "complete", "failed"],
    "external_ledger_state": [
        "CANDIDATE", "LLM_SUPPORTED", "EVIDENCE_VERIFIED", "REFUTED", "INCONCLUSIVE"
    ],
    "historical_state": [
        "EVIDENCE_VERIFIED_AT_RECORDED_REVISION", "STALE_FOR_CURRENT_REVISION"
    ],
}

EXPECTED_STATUS_RULES = [
    "producer records serialize verification_state exactly CANDIDATE",
    "assessment_decision never occupies a verification_state field",
    "external terminal states require current domain-eligible evidence",
    "historical state records both git revision and artifact revision",
    "any new repository revision stales prior current code and CUDA evidence",
]

EXPECTED_INFORMATION_POINT_FIELDS = [
    "probability", "score", "fisher", "vfe_gradient", "natural_gradient",
    "fisher_projector", "rank", "nullity", "positive_spectrum_condition_number",
    "range_residual", "inverse_rule", "used_pseudoinverse",
]

EXPECTED_OWNERSHIP_SEAMS = {
    "exact_fisher_channel_witness": {
        "symbol": "ExactFisherChannelWitness",
        "defining_module": "multiagent_elbo.finite.fisher",
        "owning_wave": "A",
        "permitted_importers": ["multiagent_elbo.finite.scale_cocycle"],
        "duplicate_definition_forbidden": True,
    },
    "information_point_constructor": {
        "symbol": "InformationPoint",
        "defining_module": "multiagent_elbo.finite.information_history",
        "owning_wave": "A",
        "constructor_fields": EXPECTED_INFORMATION_POINT_FIELDS,
        "quotient_assessment": "internal_only_no_constructor_field",
    },
    "matrix_domain_policy": {
        "symbol": "MatrixDomainPolicy",
        "defining_module": "multiagent_elbo.conditioning",
        "owning_wave": "A",
        "identity_reexport_module": "multiagent_elbo.realizations.gaussian",
        "consuming_wave": "C",
        "reexport_requirement": "same_class_object",
        "permitted_wave_c_constant": "FROZEN_FIXED_RAY_MATRIX_POLICY",
        "duplicate_definition_forbidden": True,
    },
}

EXPECTED_HISTORICAL_RECORD_CONTRACT = {
    "state_namespace": "historical_state",
    "required_fields": ["state", "git_revision", "artifact_revision"],
    "git_revision_format": "40_lowercase_hex_sha1",
    "artifact_revision_requirement": "nonempty_concrete_revision",
}

EXPECTED_SURFACES_CANONICAL_SHA256 = (
    "99123af315876e39134c3919f7297a7a3a6023e13041a7ba80e9921b9998b399"
)
EXPECTED_SCHEMA_MIGRATIONS_CANONICAL_SHA256 = (
    "9e76f4d3a2bd4632285fafd2aa02ba3908afa7ff3dc064fc6f1c1275f793d71c"
)
EXPECTED_FAILURE_ORDER_CANONICAL_SHA256 = (
    "64930d6091f98cb0ed22c98266a50d338ecff909cd645a344f043f7e134f8385"
)


def _load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _canonical_sha256(value: object) -> str:
    canonical = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _verify_historical_bundle_files(bundle: dict[str, object], *, root: Path) -> None:
    for record in bundle["files"]:
        path = root / record["path"]
        data = path.read_bytes()
        if (
            len(data) != record["size_bytes"]
            or hashlib.sha256(data).hexdigest() != record["sha256"]
        ):
            raise ValueError(f"historical bundle hash mismatch: {record['path']}")


def test_remediation_evidence_schema_closes_generic_discriminators() -> None:
    schema = _load_json(REMEDIATION_EVIDENCE_SCHEMA_PATH)
    assert isinstance(schema, dict)
    assert schema['additionalProperties'] is False
    assert schema['properties']['wave'] == {'enum': EXPECTED_REMEDIATION_WAVES}
    index_file = schema['$defs']['index_file']
    assert index_file['additionalProperties'] is False
    assert index_file['properties']['kind'] == {'enum': EXPECTED_EVIDENCE_KINDS}


def test_remediation_evidence_schema_has_dynamic_dependencies_and_policy() -> None:
    schema = _load_json(REMEDIATION_EVIDENCE_SCHEMA_PATH)
    assert isinstance(schema, dict)
    properties = schema['properties']
    assert properties['dependency_inputs'] == {
        'type': 'array',
        'minItems': 1,
        'description': (
            'Dependency path uniqueness and case-fold aliases are enforced '
            'by the production evidence-index validator.'
        ),
        'items': {'$ref': '#/$defs/file_record'},
    }
    policy = properties['tested_input_policy']
    assert policy['additionalProperties'] is False
    assert policy['required'] == [
        'schema_version',
        'selection_rules',
        'exclusion_rules',
        'inputs',
    ]
    assert policy['properties'] == {
        'schema_version': {'type': 'string', 'minLength': 1},
        'selection_rules': {
            'type': 'array',
            'uniqueItems': True,
            'items': {
                'type': 'string',
                'pattern': '^(?:prefix|exact|top_level_suffix):.+$',
            },
        },
        'exclusion_rules': {
            'type': 'array',
            'uniqueItems': True,
            'items': {
                'type': 'string',
                'pattern': '^(?:prefix|exact|top_level_suffix):.+$',
            },
        },
        'inputs': {
            'type': 'array',
            'minItems': 1,
            'description': (
                'Input path uniqueness and case-fold aliases are enforced by '
                'the production evidence-index validator.'
            ),
            'items': {'$ref': '#/$defs/file_record'},
        },
    }


def test_remediation_evidence_schema_freezes_wave0_adapter_constants() -> None:
    schema = _load_json(REMEDIATION_EVIDENCE_SCHEMA_PATH)
    assert isinstance(schema, dict)
    assert schema['allOf'] == [
        {
            'if': {
                'properties': {'wave': {'const': 'wave-0'}},
                'required': ['wave'],
            },
            'then': {
                'properties': {
                    'dependency_inputs': {
                        'type': 'array',
                        'minItems': 3,
                        'maxItems': 3,
                        'prefixItems': [
                            {
                                'properties': {'path': {'const': path}},
                                'required': ['path'],
                            }
                            for path in WAVE0_DEPENDENCY_PATHS
                        ],
                        'items': False,
                    },
                    'tested_input_policy': {
                        'properties': {
                            'schema_version': {'const': WAVE0_POLICY_SCHEMA},
                            'selection_rules': {'const': WAVE0_SELECTION_RULES},
                            'exclusion_rules': {'const': WAVE0_EXCLUSION_RULES},
                        }
                    },
                }
            },
        }
    ]


def test_audit_disposition_is_complete_closed_and_uniquely_owned():
    payload = _load_json(AUDIT_DISPOSITION_PATH)
    assert set(payload) == {
        "schema_version", "program_design_revision", "audit_baseline_revision", "items"
    }
    assert payload["schema_version"] == "scientific-remediation-audit-disposition-v1"
    assert payload["program_design_revision"] == EXPECTED_PROGRAM_DESIGN_REVISION
    assert payload["audit_baseline_revision"] == EXPECTED_AUDIT_BASELINE_REVISION
    assert tuple(item["audit_id"] for item in payload["items"]) == EXPECTED_AUDIT_IDS
    canonical_items = json.dumps(
        payload["items"], sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    assert hashlib.sha256(canonical_items).hexdigest() == EXPECTED_ITEMS_CANONICAL_SHA256
    records = {item["audit_id"]: item for item in payload["items"]}
    assert set(records) == set(EXPECTED_OWNERS)
    assert len(records) == len(payload["items"]) == 22
    for audit_id, wave in EXPECTED_OWNERS.items():
        assert records[audit_id]["owning_wave"] == wave
        assert records[audit_id]["initial_disposition"] == "EVIDENCE_VERIFIED_AT_AUDIT_BASELINE"
        assert records[audit_id]["final_status"] == "INCONCLUSIVE_PENDING_OWNER_WAVE"
        assert set(records[audit_id]) == {
            "audit_id", "severity", "owning_wave", "source_locations",
            "public_interfaces", "red_reproducer", "green_guard",
            "evidence_class", "initial_disposition", "final_status",
        }
        assert records[audit_id]["source_locations"]
        assert records[audit_id]["public_interfaces"]
        assert records[audit_id]["red_reproducer"]
        assert records[audit_id]["green_guard"]


def test_compatibility_inventory_names_every_frozen_surface():
    payload = _load_json(COMPATIBILITY_PATH)
    assert set(payload) == {"schema_version", "surfaces"}
    assert payload["schema_version"] == "scientific-remediation-compatibility-v1"
    surfaces = payload["surfaces"]
    surface_ids = [item["surface_id"] for item in surfaces]
    assert surface_ids == sorted(REQUIRED_SURFACE_IDS)
    assert set(surface_ids) == REQUIRED_SURFACE_IDS
    assert len(surfaces) == len(REQUIRED_SURFACE_IDS) == 100
    assert all(set(item) == {
        "surface_id", "kind", "legacy_symbol_or_field", "module_or_schema",
        "owning_wave", "migration", "compatibility", "package_exports",
    } for item in surfaces)
    assert {item["migration"] for item in surfaces} == EXPECTED_MIGRATIONS
    assert all(item["migration"] in EXPECTED_MIGRATIONS for item in surfaces)
    assert all(item["module_or_schema"] and "|" not in item["module_or_schema"]
               for item in surfaces)
    assert all(isinstance(item["package_exports"], list) for item in surfaces)
    assert _canonical_sha256(surfaces) == EXPECTED_SURFACES_CANONICAL_SHA256


def test_states_schema_migrations_and_ownership_seams_are_closed():
    payload = _load_json(STATUS_FAILURE_PATH)
    assert set(payload) == {
        "schema_version", "states", "status_rules", "historical_state_record_contract",
        "migrations", "ownership_seams", "failure_order",
    }
    assert payload["schema_version"] == "scientific-remediation-status-failure-v1"
    assert payload["states"] == EXPECTED_STATES
    assert list(payload["states"]) == list(EXPECTED_STATES)
    assert payload["status_rules"] == EXPECTED_STATUS_RULES
    assert payload["historical_state_record_contract"] == EXPECTED_HISTORICAL_RECORD_CONTRACT
    assert payload["ownership_seams"] == EXPECTED_OWNERSHIP_SEAMS

    migrations = payload["migrations"]
    assert len(migrations) == 26
    assert len({item["schema"] for item in migrations}) == 26
    assert all(set(item) == {
        "schema", "owning_wave", "reader_behavior", "writer_behavior",
        "rewrite_behavior", "promotion_behavior",
    } for item in migrations)
    assert _canonical_sha256(migrations) == EXPECTED_SCHEMA_MIGRATIONS_CANONICAL_SHA256

    legacy_schemas = {
        "fisher-recovery-v1", "metric-record-v1", "legacy-run-manifest-v1",
        "legacy-run-observation-v1", "legacy-figure-manifest-v1",
        "worker-protocol-v1", "worker-protocol-v2", "worker-result-v1",
        "worker-result-v2",
    }
    migration_by_schema = {item["schema"]: item for item in migrations}
    for schema in legacy_schemas:
        assert migration_by_schema[schema]["rewrite_behavior"] == "never"
        assert migration_by_schema[schema]["promotion_behavior"] == "never"


def test_producer_and_ledger_states_are_disjoint():
    payload = _load_json(STATUS_FAILURE_PATH)
    assert payload["states"]["producer_verification_state"] == ["CANDIDATE"]
    assert payload["states"]["assessment_decision"] == ["fail", "inconclusive", "pass"]
    assert payload["states"]["external_ledger_state"] == [
        "CANDIDATE", "LLM_SUPPORTED", "EVIDENCE_VERIFIED", "REFUTED", "INCONCLUSIVE"
    ]
    assert payload["states"]["historical_state"] == [
        "EVIDENCE_VERIFIED_AT_RECORDED_REVISION", "STALE_FOR_CURRENT_REVISION"
    ]
    assert "EVIDENCE_VERIFIED" not in payload["states"]["producer_verification_state"]


def test_effect_order_covers_every_frozen_entry_point_exactly():
    payload = _load_json(STATUS_FAILURE_PATH)
    failure_order = payload["failure_order"]
    entry_points = [item["entry_point"] for item in failure_order]
    assert set(entry_points) == REQUIRED_EFFECT_ENTRY_POINTS
    assert len(entry_points) == len(set(entry_points)) == 33
    assert all(set(item) == {
        "entry_point", "owning_wave", "validation_order", "last_permitted_effect",
        "negative_controls",
    } for item in failure_order)
    assert all(item["validation_order"] and item["negative_controls"]
               for item in failure_order)
    assert all(all(isinstance(token, str) and token for token in item["validation_order"])
               for item in failure_order)
    assert all(all(isinstance(token, str) and token for token in item["negative_controls"])
               for item in failure_order)
    assert all(item["last_permitted_effect"] for item in failure_order)
    assert _canonical_sha256(failure_order) == EXPECTED_FAILURE_ORDER_CANONICAL_SHA256


def test_historical_fixed_ray_bundles_are_complete_and_byte_pinned():
    payload = _load_json(HISTORICAL_BUNDLES_PATH)
    assert set(payload) == {"schema_version", "bundles"}
    assert payload["schema_version"] == "historical-fixed-ray-bundles-v1"

    bundles = {item["bundle_id"]: item for item in payload["bundles"]}
    assert set(bundles) == set(EXPECTED_HISTORICAL_BUNDLES)
    assert len(bundles) == len(payload["bundles"]) == 2

    for bundle_id, expected in EXPECTED_HISTORICAL_BUNDLES.items():
        bundle = bundles[bundle_id]
        assert set(bundle) == {
            "bundle_id", "legacy_schema", "historical_git_revision",
            "limitations", "files",
        }
        assert bundle["legacy_schema"] == "observed-v1"
        assert bundle["historical_git_revision"] == expected["historical_git_revision"]
        assert bundle["limitations"] == EXPECTED_HISTORICAL_LIMITATION
        assert len(bundle["files"]) == expected["file_count"]
        inventory_paths = [record["path"] for record in bundle["files"]]
        source_dir = ROOT / expected["path_prefix"]
        source_paths = sorted(
            path.relative_to(ROOT).as_posix()
            for path in source_dir.rglob("*")
            if path.is_file()
        )
        assert inventory_paths == source_paths
        assert all(
            set(record) == {"path", "size_bytes", "sha256"}
            and record["path"].startswith(expected["path_prefix"])
            for record in bundle["files"]
        )
        _verify_historical_bundle_files(bundle, root=ROOT)


def test_remediation_readme_preserves_status_and_revision_boundaries():
    text = README_PATH.read_text(encoding='utf-8')
    for phrase in (
        'Wave 0 does not remediate an audit defect',
        'producer verification_state is exactly CANDIDATE',
        'historical bundles are never upgraded',
        'candidate evidence',
        'exact-child closure evidence',
    ):
        assert phrase in text


def test_historical_fixed_ray_bundle_hash_drift_is_rejected(tmp_path: Path):
    payload = _load_json(HISTORICAL_BUNDLES_PATH)
    bundle = next(
        item
        for item in payload["bundles"]
        if item["bundle_id"] == "gaussian-confirmatory-fcb2c49"
    )
    source = ROOT / "docs" / "verification" / "evidence" / (
        "2026-08-10-gaussian-confirmatory-fcb2c49"
    )
    copied = tmp_path / "docs" / "verification" / "evidence" / source.name
    shutil.copytree(source, copied)

    target = copied / "config.json"
    data = target.read_bytes()
    target.write_bytes(bytes([data[0] ^ 1]) + data[1:])

    with pytest.raises(ValueError, match="historical bundle hash mismatch"):
        _verify_historical_bundle_files(bundle, root=tmp_path)
