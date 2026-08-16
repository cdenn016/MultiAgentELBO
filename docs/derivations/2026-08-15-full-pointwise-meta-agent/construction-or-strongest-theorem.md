<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Construction or strongest theorem

## Task-5 strongest verified pre-release theorem

Fix a nonempty finite active set (I), one (r_*\in\mathcal U_A), one structural datum (X), and (X_A=\chi_A(X)). Let (\mathsf O,\mathsf Y_I,\mathsf B_A,\mathsf M_A,\boldsymbol\Xi_A,\mathsf H_A) be nonempty standard-Borel spaces and put

\[
\mathsf Z_A=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A.
\]

Keep (X,X_A) outside the random channel. Let (\mathbb P_I(Do,DY\mid X)) be a fixed normalized generative joint, let (o\mapsto\boldsymbol\Pi_{I,o,X}) be a selected measurable regular-conditional kernel derived from it, and at one admitted (o) let (\mathbb Q_{I,o,X}\ll\boldsymbol\Pi_{I,o,X}) be normalized and correlated. Declare a sigma-finite observation reference and one density representative (p_X) with (0<p_X(o)<\infty). Let

\[
C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A
\]

be one normalized measurable channel fixed independently of recognition, posterior, recognition parameters, and realized observation. It leaves the observation coordinate unchanged.

Under those hypotheses, the following statements are established by `evidence/direct-derivation.md`.

1. The laws

\[
\begin{aligned}
\mathbb P_A(do,dz\mid X)
&=\int C_A(Y,dz)\mathbb P_I(do,dY\mid X),\\
\boldsymbol\Pi_{A,o,X}&=\boldsymbol\Pi_{I,o,X}C_A,\\
\mathbb Q_{A,o,X}&=\mathbb Q_{I,o,X}C_A
\end{aligned}
\]

are normalized. The parent observation marginal equals the fine one. A bounded-test-function calculation at the observation-kernel level proves that (o\mapsto\boldsymbol\Pi_{A,o,X}) is a selected parent posterior version before specialization to the admitted (o). Moreover,

\[
\mathbb Q_{A,o,X}\ll\boldsymbol\Pi_{A,o,X}.
\]

2. A parent evaluator is concretely a jointly measurable normalized family

\[
(m_A,\xi_A,E)\mapsto K^{X_A}_{A,m_A}(\xi_A;E),
\qquad E\subseteq\mathsf B_A\times\mathsf O\times\mathsf H_A.
\]

There are two valid tiers. First, a selected disintegration of (\mathbb P_A) proves existence of a normalized jointly measurable induced family and gives compatibility by construction; this is the evaluator-existence conclusion. Second, a family predeclared independently of (\mathbb P_A) is supplied as a normalized jointly measurable hypothesis and separately requires the explicit hypothesis that it agrees almost surely with the selected conditional of ((B_A,O,H_A)) given ((M_A,\Xi_A)). Under the induced conclusion or the conditional predeclared seam,

\[
\mathbb P_A(db_A,do,dh_A\mid\xi_A,m_A,X)
=K^{X_A}_{A,m_A}(\xi_A;db_A,do,dh_A)
\]

hold for the parent ((M_A,\Xi_A)) marginal almost surely. Standard-Borel disintegration does not validate an arbitrary predeclared evaluator, choose its null extension canonically, make evaluation injective, or regularize the quotient of presentations.

3. With (\mathbb P_A^Z(D\mid X)=\mathbb P_A(\mathsf O\times D\mid X)), the recognition marginals (q_A^b,q_A^m), latent-prior marginals (p_A^b,p_A^m), and posterior marginals (\boldsymbol\Pi_{A,o,X}^b,\boldsymbol\Pi_{A,o,X}^m) are exactly the corresponding coordinate pushforwards of (\mathbb Q_{A,o,X}), (\mathbb P_A^Z(\cdot\mid X)), and (\boldsymbol\Pi_{A,o,X}). These identities do not reconstruct a joint law: the exact finite witnesses in `evidence/counterexample-proofs.md` and `evidence/finite-nongaussian-output.json` verify marginal nonuniqueness and the failure of marginal invariance to imply joint invariance.

4. Let the recognition and posterior joint lifts attach the same (C_A), and disintegrate each lift in (Y) conditional on (z). Then the additive identity in ([0,+\infty]) is

\[
\operatorname{KL}(\mathbb Q_{I,o,X}\Vert\boldsymbol\Pi_{I,o,X})
=\operatorname{KL}(\mathbb Q_{A,o,X}\Vert\boldsymbol\Pi_{A,o,X})
+\Delta_A(o,X),
\]

where

\[
\Delta_A(o,X)=\int
\operatorname{KL}\!\left(
\widehat{\mathbb Q}_{I,o,X}(dY\mid z)
\middle\Vert
\widehat{\boldsymbol\Pi}_{I,o,X}(dY\mid z)
\right)\mathbb Q_{A,o,X}(dz)\geq0.
\]

The common finite evidence representative gives

\[
\mathcal F_I=\mathcal F_A+\Delta_A
\]

as an extended additive identity, without subtracting infinities. If the fine KL is finite, the ordinary real difference is (\mathcal F_I-\mathcal F_A=\Delta_A), and

\[
\Delta_A=0
\quad\Longleftrightarrow\quad
\widehat{\mathbb Q}_{I,o,X}(dY\mid z)
=\widehat{\boldsymbol\Pi}_{I,o,X}(dY\mid z)
\quad\mathbb Q_{A,o,X}\text{-almost surely}.
\]

On this finite tier, the zero-defect condition is also equivalent to the existence of one normalized pairwise recovery kernel that recovers both declared fine laws. Family-wide common recovery requires simultaneous hypotheses for every family member; (+\infty=+\infty) has no recovery consequence.

5. The frozen target declares a holonomy branch; it does not assert logical exclusivity, because blindness and retention can coexist for different retained coordinates or quotient levels. On the blindness branch, covariance is conditional on typed source/target groupoid actions, covariance of the full fine generative and recognition laws, a jointly compatible selected-posterior version family, (C_A) equivariance, and evaluator covariance. Under those hypotheses the parent generative, posterior, and recognition laws are covariant. Same-slice invariance follows only for isotropy arrows fixing the declared (o,X) and selected versions. On the retention branch, if (\mathsf H_A) and (C_A) retain component roots, raw root-framed holonomy, and dressed boundary marks, the parent full laws retain those records jointly and make no holonomy-blind claim. Exact finite witnesses separately verify that trivial holonomy does not force agent agreement and that invariant marginals do not force invariant dependence.

6. The construction is static. In a separately declared differentiable special case, the exact moving-map defect is

\[
\delta_t=\partial_tc_t+Dc_tV_t-\overline V_t\circ c_t.
\]

For Markov evolution, exact closure is the semigroup intertwining (T_tU=U\overline T_t). A generator identity is an alternative criterion only on a declared invariant domain or core, with hypotheses that both operators generate the stated semigroups and that the identity lifts uniquely to semigroup intertwining. Neither condition follows from the static theorem. Autonomy, selected membership, Wheelerian feedback, sustained nonequilibrium, and physical time remain OPEN.

## Proof architecture and evidence

Kernel integration proves normalization and preserves the observation marginal. Equation-level disintegration against bounded observation and parent test functions proves the posterior version globally. Null-set transfer through the same kernel proves parent absolute continuity. A second standard-Borel disintegration isolates the evaluator seam and proves only its induced or explicitly compatible tier. Coordinate test functions prove the marginal identities.

For VFE, the joint-lift Radon--Nikodym derivative is the fine derivative (d\mathbb Q_I/d\boldsymbol\Pi_I). Relative-entropy disintegration factors it into parent and conditional derivatives and produces two nonnegative terms; no infinite quantity is subtracted. KL's zero criterion proves the discarded-conditional equality. The posterior conditional supplies the forward recovery direction, while data processing through a separately assumed common reverse kernel proves the finite converse. Equivariant substitution in the parent defining integrals proves full-law covariance, and ordinary differentiation or operator intertwining gives the typed dynamic formulas.

The direct derivation has SHA-256 `2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a`; the finite counterexample proof has SHA-256 `59c38ed4181b2f8fbf2b573c79cb7257516c7e2d91e44dbea870c953406de6fc`; and the deterministic arithmetic witness has SHA-256 `ca79ea94822e74ad1e7fb3257d0ea852a609a9102be0e49a302687ad1612c062`. `claim-ledger.json` records all seventeen static target ancestors plus the dynamics boundary claim as `EVIDENCE_VERIFIED`. The extended-valued KL chain rule is a strengthening; the frozen target's finite-KL identity and equality/recovery statement are its explicit corollary. Computation and agent agreement are not used as mathematical closure.

## Final release status

The mixed claim `target` is `EVIDENCE_VERIFIED`, and `release.json` records `COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS` with `certificate_claim` equal to `target`. Direct derivation and exact counterexamples close every static ancestor; independent reconstruction and semantic oracle erasure pass. Two of the four domain reviews (information/VFE `c291869c…`, dynamics/scope `71401ff1…`) are current `APPROVE` records with Critical/High/Medium counts of zero. The other two (probability/kernel `14f7f00f…`, gauge/holonomy `431a63b0…`) are `BOUND_STALE_PRE_INTEGRATION`: they bind canonical `Theory/06` and `Theory/07b` bytes that were edited after they approved, so their own post-review-mutation falsifiers are met and their approvals do not extend to the released revision. The sixteen adversarial dispositions are recorded but are **not** evidence for the theorem, since fifteen of the sixteen have an outcome fixed by a frozen premise or an explicit non-claim. See `POST-RELEASE-CORRECTIONS.md`.

Review provenance remains one-way. The domain reviews bind the corrected pre-review mathematical/payload snapshot at Git `HEAD add1a69f2b83550d13abd330c13f4b4e8e9138b9`; the Fix Round 1 post-commit review binds the prior final-release snapshot at Git `HEAD 1b18842d6f853ee32c2b4f8a1741b1738ce9890e`; and the repaired final snapshot binds the finding-driven changes. `evidence/release-provenance.json` records all three snapshots without asserting a mutual raw-hash fixed point.

The theorem is pointwise in one fixed (X). It makes no claim of cross-(X) sufficiency through (X_A), a smooth or Gaussian ambient family, a canonical presentation quotient, membership selection, patchwise gluing over (\mathcal U_A), a pair of parent sections, a full geometric meta-agent, canonical coarse-channel or partition selection, the downstream comparison theorem, autonomy, nonequilibrium, ontic action, a unique latent DAG or unique microscopic physics, or physical time. `DYNAMICS-SCOPE` is a verified boundary/nonclaim, not a target ancestor, because the frozen target explicitly excludes dynamics from its static closure.
