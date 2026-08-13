# U(1) record-moment verification evidence

This directory binds the executable reproduction of the repaired finite U(1) two-path witness.

- `results.json` records the witness SHA-256, Python and NumPy versions, exact returned values,
  scope flags, and captured stdout.
- `pytest.xml` records the five focused implementation checks and their machine-readable totals.

The mathematical certificate is separate:
`docs/derivations/2026-08-13-u1-record-moment-derivation.md`. The machine run confirms that the
implementation realizes those formulas at the recorded source hash; it does not prove the formulas.

The historical F5 adjudication tested an earlier witness and is explicitly superseded for current
numerical details by `docs/reviews/adjudication-2026-08-13/README.md`.
