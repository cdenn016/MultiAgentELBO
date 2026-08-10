# Scale/RG/CUDA Session 6 Review

Date: 2026-08-09

Review scope: exact scale composition, Gaussian fixed-ray pilot, and isolated worker/controller implementation

## Review conclusion

The CPU implementation is internally consistent with the frozen finite scope and the shared laboratory contracts. Exact scale identities have independent literal oracles and mutation controls. The Gaussian lane is correctly bounded as a non-heavy four-job pilot. The CUDA implementation is present but its scientific parity claim is not closed because execution was prohibited while the GPU was busy.

## Scope and theory checks

- The immutable two-scale fixture is validated and left unchanged. The third scale is a separate self-identified extension artifact.
- Markov channels are normalized and recognition-independent. Direct/staged law, conditional action, and posterior bridge composition are checked exactly.
- Comparison orientation is `I_target C I_source^-1`; derivative factors carry source/target level and tangent type, invalid adjacency is rejected, and the valid sequence is ordered as a nonautonomous cocycle.
- The retained beta residual preserves its sign and typed identifications. Difference, identified-projection, and native-transport forms agree exactly. Three sign-sensitive base Fisher residual forms also agree.
- A pairwise fine log-likelihood is passed through a declared exact coarse channel before Möbius decomposition. The resulting triple coefficient is `-0.32394711573301693`; the pairwise-only coarse reconstruction fails by its magnitude.
- All six additional semantic artifacts frozen by the registry are published and declared through `RunStore` with exact inputs or sufficient data for independent recomputation.
- The Gaussian fixed-ray code checks `M0` is SPD, both maps are primitive, the Perron ray factorizes, and the declared basin is finite. Projective stabilization is not reported as selecting `M0` or proving an infinite-hierarchy attraction theorem.
- Every emitted metric carries `theorem_status`, `verification_state`, and `claim_origin`; recomputation arrays are retained through `RunStore`.

## Controller-worker checks

- The Python 3.14 controller imports neither Torch nor CUDA and leaves NumPy RNG state unchanged at import.
- The standalone Python 3.12 worker validates the versioned JSON/NPZ envelope independently, including job, schema, exact scientific output inventory, request-derived output shape/dtype, per-array digest, file digest, environment-lock digest, request-response binding, and effective backend/dtype.
- CPU worker tests cover remainder batches, zero rows, noncontiguous controller inputs, batch-schedule invariance, a near-boundary SPD matrix direction with condition number `1e10`, and mutated output rejection.
- A CUDA request made through the unpinned Python 3.14 executable fails before creating its worker artifact directory.
- A pinned CUDA request with `CUDA_VISIBLE_DEVICES=-1` fails in an isolated worker preflight before creating its job directory, input NPZ, or request JSON.
- The frozen provenance validator requires live driver, CUDA runtime, cuDNN, cuBLAS/cuBLASLt file versions and hashes, Torch config, actual kernel strategy, runtime, retry lineage, peak memory, and lock consistency for CUDA. CPU records carry explicit null CUDA identities and the actual rowwise strategy. Missing fields or lock drift are rejected.
- CUDA code configures `CUBLAS_WORKSPACE_CONFIG=:4096:8` before process creation, deterministic algorithms before the first CUDA operation, and TF32 disabled. The hidden-device preflight exercised only fail-closed availability detection; no CUDA kernel or device scientific operation was executed.

## Evidence boundary

`EVIDENCE_VERIFIED` on scale metrics means the current exact implementation checks and literal oracles closed those finite implementation claims. `EVIDENCE_VERIFIED` on pilot metrics means the saved pilot arrays reproduce the reported finite values. Neither designation elevates the Gaussian conjecture to a theorem.

The CUDA-dependent metric remains `OPEN / INCONCLUSIVE / APPLICATION_SPECIFIC`. Closure requires a later fresh idle-device check, explicit operator opt-in, the pinned Python 3.12 CUDA worker, recorded RTX 5090 identity/capability and Torch/CUDA/library state, plus the full float64 three-lane sentinel parity matrix. Until then, no CUDA performance, parity, or scientific confirmation claim is authorized.

## Required integration follow-up

1. When the RTX 5090 is demonstrably idle and the operator opts in, run the controller gate and float64 CUDA parity sentinel before any confirmatory job.
2. Do not run `C001`-`C030` or release `H001`-`H010` until the parity gate is complete.
3. Preserve the preregistered thresholds even though the pilot window slopes do not meet the practical `-0.02` threshold.
4. Treat bfloat16 as exploratory only; the present worker deliberately rejects an unimplemented bfloat16 payload encoding rather than silently using float32.
