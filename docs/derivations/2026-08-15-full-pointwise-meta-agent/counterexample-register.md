<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Counterexample register

All registered witnesses are finite and categorical. Their direct proofs are in `evidence/counterexample-proofs.md`; `evidence/finite-nongaussian-output.json` is deterministic arithmetic corroboration only.

## CE-1: identical fair marginals, distinct singular joints

The fair correlated law on ((0,0),(1,1)) and the fair anticorrelated law on ((0,1),(1,0)) have identical belief and model marginals but distinct, disjoint joint supports. Both directed joint KL divergences are (+\infty).

Status: exact counterexample; closes `NEG-MARGINAL-DETERMINATION`.

## CE-2: split-channel VFE failure

Set the fine recognition and posterior laws equal to the fair binary law. Push recognition through the identity channel and the posterior/generative law through the constant-zero channel. Fine forward KL is zero, while coarse recognition assigns positive mass where the coarse posterior assigns zero, so coarse forward KL and the singleton-evidence coarse VFE are (+\infty). The reverse coarse KL is only (\log2) and is not substituted.

Status: exact counterexample; closes `NEG-SPLIT-CHANNEL-VFE`. The common-channel theorem is not attacked.

## CE-3: evaluator mismatch on positive generative model mass

In the main witness, the compatible conditional evaluator is (\operatorname{ev}_A(m)=K_m) with (K_m(B=1)=1/4+m/2). The swapped normalized family (\operatorname{ev}'_A(m)=K_{1-m}) disagrees at both model points, each of which has generative parent mass (1/2), while the generative model marginal remains normalized and fair.

Status: exact counterexample; closes `NEG-MODEL-MARGINAL-EVALUATION`. Almost-sure compatibility is the repair.

## CE-4: trivial holonomy without agreement

A two-node identity-transport tree has trivial holonomy. Assigning (\operatorname{Bernoulli}(1/4)) and (\operatorname{Bernoulli}(3/4)) at its nodes leaves unequal transported laws, with either directed KL equal to (\tfrac12\log3).

Status: exact counterexample; closes `NEG-TRIVIAL-HOLONOMY-AGREEMENT`.

## CE-5: invariant marginals without invariant dependence

The one-coordinate bit flip maps the correlated fair joint law to the anticorrelated fair joint law. Each coordinate marginal remains invariant, but the full law changes. As a complementary boundary, the nonidentity bit flip stabilizes the fair one-bit law.

Status: exact counterexample; closes `NEG-MARGINAL-HOLONOMY-JOINT` and records that nontrivial holonomy can stabilize a law.

## Exact lossy witness

For (M=B=E=\{0,1\}), singleton observation, interface, and mark spaces, fixed structural (X), fair (M), evaluated Bernoulli rows (K_m(B=1)=1/4+m/2), and independent fair generative (E), recognition preserves the posterior ((M,B)) marginal and sets (E=B). The common channel retains ((B,M)). Exactly,

\[
\mathbb Q_{A,1,X}=\boldsymbol\Pi_{A,1,X},\qquad
q_A^b=q_A^m=\operatorname{Bernoulli}(1/2),
\]

\[
\operatorname{KL}(\mathbb Q_{I,1,X}\Vert\boldsymbol\Pi_{I,1,X})=\log2,
\quad
\operatorname{KL}(\mathbb Q_{A,1,X}\Vert\boldsymbol\Pi_{A,1,X})=0,
\quad
\Delta_A=\log2.
\]

The reverse fine divergence is (+\infty) and is not interchangeable with the VFE orientation. The derived prior marginals (p_A^b,p_A^m) are also fair in this singleton-observation instance but remain separately typed from the recognition marginals.

Status: exact finite non-Gaussian instance of the Task-3 construction; symbolic logarithmic values are primary.

## Task-5 release binding

The direct proof artifact is bound at SHA-256 `59c38ed4181b2f8fbf2b573c79cb7257516c7e2d91e44dbea870c953406de6fc`; the deterministic arithmetic corroboration is bound at SHA-256 `7092ec0a0dce059c2fcfc177ec288b0b708481aa9eace7a6ee657e3a1dc21e0c` and its source at SHA-256 `204effc256fcc89d9b6cbaa80d33b88eac845b7bfe2694653b0e204eb4760b48`.

All five negative claims are existential and are therefore supported by `DERIVATION` evidence with `supports: true`; none is labeled `COUNTEREXAMPLE` evidence in the verification schema. CE-2 and CE-3 refute theorems obtained by deleting the common-channel or compatibility premises, not the conditional theorem proved under those premises. CE-5 distinguishes marginal invariance from full-law invariance. CE-4 distinguishes trivial transport holonomy from equality of node laws.

The witnesses do not establish an impossibility theorem for every coarsening, a converse to data processing, evaluator uniqueness on null fibers, quotient regularity, dynamics, autonomy, ontology, or gluing. They close exactly the registered existential negative ancestors.
