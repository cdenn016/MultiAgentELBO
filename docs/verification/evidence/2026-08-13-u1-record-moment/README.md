# U(1) record-moment verification evidence

This directory binds the executable reproduction of the repaired finite U(1) two-path witness.

`manifest.json` pins the source, tests, derivation, outputs, commands, and runtime to Git revision
`52ba348f6a0fb88e2de9745bbf166e1fdb4f59f0`.

- `results.json` records the witness SHA-256, Python and NumPy versions, exact returned values,
  scope flags, and captured stdout.
- `pytest.xml` records the five focused implementation checks and their machine-readable totals.

The mathematical certificate is separate:
`docs/derivations/2026-08-13-u1-record-moment-derivation.md`. The machine run confirms that the
implementation realizes those formulas at the recorded source hash; it does not prove the formulas.

The historical F5 adjudication tested an earlier witness and is explicitly superseded for current
numerical details by `docs/reviews/adjudication-2026-08-13/README.md`.
