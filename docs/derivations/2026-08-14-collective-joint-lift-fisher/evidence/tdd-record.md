<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2","schema_version":"rigorous-theory-search/v1","target_digest":"ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2"} -->
# Strict TDD record

## RED

The test file was added before the witness existed. The first command was:

    C:/Python314/python.exe -m pytest tests/test_collective_joint_lift_witness.py -q --junitxml=C:/tmp/collective-joint-lift-red-20260814.xml

It exited 1 with 5 failed tests. Every failure was the expected
FileNotFoundError for the not-yet-created
evidence/exact_collective_witness.py. The preserved machine-readable result is
red-junit.xml.

## GREEN

After the exact standard-library Fraction witness was implemented, and again
after the off-center positivity/residual and cancelling-kernel controls were
added, the focused command exited 0:

    C:/Python314/python.exe -m pytest tests/test_collective_joint_lift_witness.py -q --junitxml=C:/tmp/collective-joint-lift-green-20260814.xml

The final focused result was 5 passed; exact machine-readable timing is retained in green-junit.xml. The preserved
machine-readable result is green-junit.xml.

The tests enumerate all 63 proper marginal subsets and every assignment
within each subset; assert exact positivity and normalization of all 64
off-center atoms; check all eight paired complements, a nonzero-scalar odd
flip negative control, and its pseudoscalar repair; check the exact center
Fisher and residual matrices; check exact positive leading principal minors
for an off-center residual; verify the record evidence, posterior, and VFE
expressions; verify the fixed-outside VFE difference and directional
differential; verify the same-marginal cancelling record kernel; and compare
two complete JSON emissions byte-for-byte.

The JUnit runs and executable are corroboration. Mathematical closure rests on
the direct derivations, not finite enumeration alone.
## Validator-bound provenance

The claim ledger binds five process artifacts independently of the theorem's
mathematical derivations: `red-junit.xml`, this `tdd-record.md`, and
`test_collective_joint_lift_witness.snapshot.py`. The snapshot is byte-for-byte
identical to the final focused test source at
`tests/test_collective_joint_lift_witness.py`; its SHA-256 is recomputed and
validated as a contained evidence artifact. The RED JUnit proves only the
recorded test-first missing-witness failure. The TDD record and test snapshot
prove process provenance, not mathematical truth.

The review remediation also followed a local RED/GREEN cycle: the updated test
first failed on the missing `direction_kind`,
the missing true agent-theta control, and the stale subgroup payload key;
review-red-junit.xml preserves that failure and the final GREEN JUnit preserves
closure.
A second remediation RED/GREEN cycle then required the agent-theta control to
accept a pair index and exercise all three declared blocks. The pre-change
TypeError and scalar-payload failure are preserved in review2-red-junit.xml;
the final GREEN covers all three exact outside-marginal and tangent checks.
