# Full Pointwise Meta-Agent Program Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish and integrate a fully typed, generally lossy pointwise probabilistic datum for a candidate meta-agent at one fixed context by pushing a declared fine generative joint, posterior, and correlated recognition law through one common recognition-independent Markov channel. Publication is a separate authorization gate.

**Architecture:** Phase 0 first freezes a repository-wide notation registry and collision gate. Phase 1 separates model-law coordinates from evaluated generative kernels and constructs the full parent probabilistic datum through one normalized coarse channel while fixed structural data remain outside it, including posterior pushforward and model-evaluation compatibility. Phase 2 proves the VFE disintegration identity and the exact full-law/channel holonomy alternatives. Comparison semantics, patchwise gluing, and participatory nonequilibrium remain separate downstream projects and receive no inherited theorem status.

**Tech Stack:** Standard-Borel probability and Markov-kernel mathematics, measure disintegration, KL/VFE chain rules, gauge/holonomy groupoids, Python 3.14 standard library (`fractions`, `decimal`, `json`, `hashlib`, `pathlib`, `re`), LaTeX/pdflatex, rigorous-theory-search release validator, verification schema 1.1, Git worktrees.

**Spec:** `docs/superpowers/specs/2026-08-15-full-pointwise-meta-agent-design.md`

## Global Constraints

- Execute on a fresh `codex/` feature branch from the then-current `origin/main`; record the exact worktree, branch, and baseline SHA in Task 1. This plan was prepared against `8c0f4d5b4116ac3883665756a451e025f0712b97`.
- Before each task, read the approved design, `Theory/SPEC.md`, and preceding commits. Use American English.
- Released derivation packages, archived audits, and prior worklog prose are immutable. Append chronology; record historical symbols as legacy aliases rather than rewriting evidence.
- General normalized laws and kernels on standard-Borel spaces are primary. Statistical manifolds require separate DQM, domination, score-integrability, and Fisher-regularity hypotheses. Multivariate Gaussians are optional computational examples only.
- Reserve `\mathscr P_G\to\mathcal C` for the principal bundle; `\mathbb P`, `\mathbb Q`, `\boldsymbol\Pi` for global laws; `\varpi` for bundle projection; and `\alpha_i^x` for receiver occupancy.
- Use agent supports `\mathcal C_i` and overlap `\mathcal U_A=\bigcap_{i\in A}\mathcal C_i`; ordinary intervention variables remain `R,E,O`.
- Established `q_i^{o,X},s_i^{o,X}` retain their dependencies. A semantic migration may use `q_i^{b;o,X},q_i^{m;o,X}`, but bare `s_i` is not globally renamed. Only explicitly law-valued `m_i` in frozen pointwise-RG passages may be a local alias; sample `m_i\in\mathsf M_i` remains a model coordinate. It evaluates to a normalized kernel `K^X_{i,m_i}` that cannot read recognition, posterior, recognition parameters, or realized observations.
- Keep structural `X` fixed and outside `C_A`, with `X_A=\chi_A(X)`. Use `\mathsf Z_A=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A` and freeze `\operatorname{ev}_A:m_A\mapsto K^{X_A}_{A,m_A}` in `\operatorname{Kern}(\boldsymbol\Xi_A,\mathsf B_A\times\mathsf O_A\times\mathsf H_A)`. Require its a.s. compatibility with the pushed parent generative conditional.
- Exactly one normalized recognition-independent `C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A` acts on fine generation, posterior, and recognition while structural `X` remains fixed. Preserve all `o,X` dependencies. Split channels define a different approximation problem.
- Fix an admitted observation/posterior version. Never evaluate an almost-sure conditional silently on a null observation slice.
- Treat `h_#q_A^x=q_A^x` only as an inherited marginal result. A holonomy-blind parent requires a declared joint action, full-law compatibility, `C_A` equivariance, and evaluation compatibility; otherwise retain roots, holonomy, and boundary marks.
- The static target is a full pointwise probabilistic datum, not yet a pair of local sections or full geometric meta-agent. Do not promote it to autonomy, dynamical RG, physical time, unique DAG/physics, or patchwise closure over `\mathcal U_A`. Use lowercase `c_t` only for a deterministic moving-map special case.
- Do not run repository pytest, import Torch, use the GPU, or launch models. Use exact standard-library recomputation, validators, static scans, and TeX builds.
- Mathematics closes only by direct derivation, formal proof, or hypothesis-mapped theorem. Computation and agent agreement corroborate but do not prove. Missing evidence yields `INCONCLUSIVE`.
- New `docs/derivations/2026-08-15-full-pointwise-meta-agent/**` files use LF; `Theory/**` retains CRLF. Any tracked edit after release/ledger pin invalidates closure.
- The Research wiki is read-only here. Offer a separate post-publication ingest; write only after explicit approval.

## File Map

- New proof package: `docs/derivations/2026-08-15-full-pointwise-meta-agent/`, including all nine rigorous-theory root artifacts.
- Notation evidence: `evidence/notation-standard.md`, `notation-registry.json`, `notation_scan.py`, and `notation-collision-report.json`.
- Proof evidence: `evidence/direct-derivation.md`, `counterexample-proofs.md`, `finite_nongaussian_witness.py`, and `finite-nongaussian-output.json`.
- Review evidence: `evidence/independent-reconstruction.md`, `oracle-erasure.md`, `adversarial-attacks.md`, and `evidence/reviews/`.
- Canonical integration: `Theory/SPEC.md`, `Theory/appendix_notation.tex`, `Theory/03_probability.tex`, `Theory/06_general_coarsegraining.tex`, `Theory/07b_agent_network_rg.tex`, `Theory/appendix_claim_ledger.tex`, `solid_RG_theory.md`, `overview.md`, `docs/STATUS.md`, and the August 12 worklog.

---

### Task 1: Freeze the Approved Design and Proof Contract

**Files:**
- Create: approved design, this plan, and all nine new package-root artifacts
- Modify: `.gitattributes`

**Interfaces:**
- Consumes: the released 2026-08-14 pointwise package and fetched `origin/main`.
- Produces: one digest-bound mixed target and additive proof workspace.

- [ ] **Step 1: Create and record an isolated baseline.**

Run `git fetch`, create a fresh worktree/branch from `origin/main`, then record absolute path, branch, and SHA in `problem-contract.json`.

```powershell
git status --short --branch
git rev-parse HEAD
git log -1 --oneline origin/main
git merge-base --is-ancestor origin/main HEAD
```

Expected: clean recorded baseline and zero ancestor-check exit.

- [ ] **Step 2: Add the package EOL rule.**

```gitattributes
docs/derivations/2026-08-15-full-pointwise-meta-agent/** text eol=lf
```

- [ ] **Step 3: Scaffold the package.**

```powershell
& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\scaffold_run.py' --date 2026-08-15 --slug full-pointwise-meta-agent 'docs\derivations'
```

- [ ] **Step 4: Freeze exact quantifiers.**

Use `quantifier_class=MIXED` and `negative_certificate_kind=COUNTEREXAMPLE`. The conditional-universal affirmative target quantifies over declared standard-Borel spaces, normalized fixed `\mathbb P_I(\cdot\mid X)`, admitted regular `o`, `\boldsymbol\Pi_{I,o,X}`, `\mathbb Q_{I,o,X}\ll\boldsymbol\Pi_{I,o,X}`, normalized recognition-independent `C_A`, parent `\mathsf M_A`, `\boldsymbol\Xi_A`, `\mathsf H_A`, normalized measurable `\operatorname{ev}_A`, and a.s. evaluation compatibility. It covers parent normalization, posterior identity, derived marginals, VFE chain/equality, and holonomy alternatives. Negative conjuncts are Task 4 counterexamples. Exclude a full geometric meta-agent, canonical selection, reconstruction from marginals, Gaussian generality, autonomy, agency, nonequilibrium, ontic actions, unique physics, and patchwise gluing.

- [ ] **Step 5: Validate and commit frozen input.**

```powershell
& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py' --mode checkpoint 'docs\derivations\2026-08-15-full-pointwise-meta-agent'
git diff --check
git ls-files --eol -- '.gitattributes' 'docs/superpowers/**' 'docs/derivations/2026-08-15-full-pointwise-meta-agent/**'
git commit -m "docs: design full pointwise meta-agent program"
```

### Task 2: Establish Phase 0 Notation and Collision Control

**Files:**
- Create: all four notation evidence files
- Modify: `Theory/SPEC.md` section 3 and `Theory/appendix_notation.tex`
- Modify only for canonical consistency: `Theory/01_introduction.tex`, `02_geometry.tex`, `03_probability.tex`, `05c_pullback_geometry.tex`, `05d_relational_inference.tex`, `overview.md`, `solid_RG_theory.md`, `docs/STATUS.md`, and active worklog section

**Interfaces:**
- Consumes: approved Phase 0 table.
- Produces: normative symbol registry and reproducible active-source collision classification.

- [ ] **Step 1: Write the notation standard.**

Freeze:

```text
principal object      mathscr P_G -> mathcal C
global laws           mathbb P_(I/A)(.|X), mathbb Q_(I/A,o,X), boldsymbol Pi_(I/A,o,X)
sections              q_i^{b;o,X}, q_i^{m;o,X}; preserve q_i^{o,X}, s_i^{o,X}
model point/kernel    m in mathsf M_i, ev_i(m)=K_(i,m)
supports/overlap      mathcal C_i, mathcal U_A=intersection_i mathcal C_i
structural/interface  X, X_A=chi_A(X), xi_A in boldsymbol Xi_A
receiver/event        alpha_i^x, eta_ij^x
bundle projection     varpi_x only
coarse channel        C_A as Markov kernel
deterministic map     c_t only in the smooth moving-map special case
intervention chain    R -> E -> O
action                 mathscr S
```

Record established `q_i^{o,X},s_i^{o,X}` as typed source notation; do not globally rename bare `s_i`. Record only explicitly law-valued frozen-RG `m_i`, `Q_q,Q_m`, and principal-bundle `P` as scoped legacy aliases. Preserve sample `m_i`, structural `X`, and observation `o`. Bare `P,Q` remain local dummy measures only.

- [ ] **Step 2: Create the JSON registry.**

Every symbol has `canonical`, `concept`, `type`, `domain_codomain`, `scope`, `status`, `canonical_sources`, `legacy_aliases`, and `forbidden_uses`. Top level has `schema_version`, `active_roots`, `immutable_roots`, and sorted `symbols`. Reject a canonical token carrying multiple types, duplicate canonical/type entries, and one alias mapping to several canonical symbols in one scope. Alias records are explicitly typed and scoped.

```json
{"canonical":"\\mathbb P_A","concept":"parent generative joint","type":"probability law on observation times parent latent-model space","domain_codomain":"P(O x Z_A)","scope":"global","status":"DEFINITION","canonical_sources":["Theory/SPEC.md","Theory/appendix_notation.tex"],"legacy_aliases":["P_A"],"forbidden_uses":["principal bundle","independent belief marginal"]}
```

- [ ] **Step 3: Implement the fail-closed scanner.**

```python
def load_registry(path: Path) -> dict[str, object]: ...
def scan_active_sources(root: Path, registry: dict[str, object]) -> list[dict[str, object]]: ...
def classify_occurrence(path: str, line: int, token: str, registry: dict[str, object]) -> str: ...
def validate_registry(registry: dict[str, object]) -> list[str]: ...
def main(argv: Sequence[str] | None = None) -> int: ...
```

Accept `--registry`, `--root`, `--output`, `--self-test`. Scan `Theory/`, start guide, overview, STATUS, active specs/plans, and worklog; exclude audits/generated TeX/released packages except current. Emit sorted `canonical`, `documented_legacy`, `immutable_evidence`, and `unclassified_collision`. Fail on invalid registry, unclassified active collision, occupancy `\varpi_i`, or new global bare `P_A,Q_A`.

- [ ] **Step 4: Migrate semantically.**

Update SPEC/notation appendix first. Replace principal `P` only when typed as principal bundle; retain dummy measures/generative laws and geometric `\varpi_i`. Introduce the canonical symbols with exact types. Migrate other active sources or add scanner-recognized local legacy declarations. Never global-replace blindly.

- [ ] **Step 5: Self-test and scan.**

Reject fixtures using `\varpi_i` as occupancy, bare global `P_A`, law-valued sample `m_i`, `C_A` as matrix and kernel, and one duplicate alias; accept a correctly typed sample `m_i`. Accept immutable historical occurrences and allowlisted lemma-local `P,Q`.

```powershell
& 'C:\Python314\python.exe' 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\notation_scan.py' --self-test
& 'C:\Python314\python.exe' 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\notation_scan.py' --registry 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\notation-registry.json' --root . --output 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\notation-collision-report.json'
Get-FileHash -Algorithm SHA256 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\notation-collision-report.json'
```

Expected: no unclassified collisions, nonempty documented legacy inventory, sorted deterministic JSON, one LF.

- [ ] **Step 6: Checkpoint and commit.**

Run notation scan, JSON parsing, diff/EOL/C0/BOM checks, package checkpoint validation, and confirm no prior package changed. Commit `docs: standardize meta-agent notation`.

### Task 3: Prove the Full Common-Channel Pointwise Datum

**Files:**
- Create: `evidence/direct-derivation.md`
- Modify: package theorem, claim ledger, dependency DAG, and approach registry

**Interfaces:**
- Consumes: notation registry and inherited coarse-channel lemmas.
- Produces: direct proof of the static full parent.

- [ ] **Step 1: Type spaces and fine laws.**

Fix structural `X`, set `X_A=\chi_A(X)`, and declare nonempty standard-Borel `\mathsf O`, `\mathsf Y_I`, `\mathsf B_A`, `\mathsf M_A`, `\boldsymbol\Xi_A`, and `\mathsf H_A`, with `\mathsf Z_A=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A`. Structural data remain outside the random channel. State sigma-algebras, projections, normalized `\mathbb P_I(Do,DY\mid X)`, admitted `\boldsymbol\Pi_{I,o,X}`, and `\mathbb Q_{I,o,X}\ll\boldsymbol\Pi_{I,o,X}` with finite/extended KL. Each displayed `q_i^b,q_i^m` is a declared `\mathbb Q` marginal, never a presumed joint lift.

- [ ] **Step 2: Prove one model-evaluation type and compatibility.**

Freeze `ev_A: M_A -> Kern(Xi_A, B_A x O_A x H_A)`, parameterized only by fixed
`X_A`, and require joint measurability/normalization of `K^(X_A)_(A,m_A)`. Prove

```text
mathbb P_A(db_A,do,dh_A | xi_A,m_A,X)
  = K^(X_A)_(A,m_A)(xi_A; db_A,do,dh_A)
```

for the parent `(Xi_A,M_A)` marginal almost surely. Standard-Borel disintegration supplies only an
a.s. induced version, not a unique null extension, injective presentation, smooth quotient, or
ontology. If presentations are quotiented by equal evaluated kernels, separately prove the
quotient is standard Borel (and smooth when claimed); otherwise retain presentations.

- [ ] **Step 3: Construct the parent triple.**

```text
mathbb P_A(do,dz|X)=integral C_A(Y,dz) mathbb P_I(do,dY|X)
boldsymbol Pi_(A,o,X)=boldsymbol Pi_(I,o,X) C_A
mathbb Q_(A,o,X)=mathbb Q_(I,o,X) C_A
```

Prove normalization/measurability and, via bounded test functions and the selected fine disintegration, that `\boldsymbol\Pi_{A,o,X}` is a posterior version of `\mathbb P_A` almost everywhere in admitted `o`.

- [ ] **Step 4: Derive marginals.**

Define `q_A^b=(pr_b)_#\mathbb Q_{A,o,X}`, `q_A^m=(pr_m)_#\mathbb Q_{A,o,X}`, generative-conditional marginals `p_A^b,p_A^m`, and posterior marginals `\boldsymbol\Pi_{A,o,X}^b,\boldsymbol\Pi_{A,o,X}^m`. Distinguish conditional `\mathbb P_{A,o}` from joint `\mathbb P_A`. Prove projection identities; state that marginals do not reconstruct dependence.

- [ ] **Step 5: Prove lossy VFE closure.**

Disintegrate the two joint channel lifts and prove for finite fine KL:

```text
F_I(o,X;mathbb Q_(I,o,X))=F_A(o,X;mathbb Q_(A,o,X))+Delta_A(o,X)
Delta_A=integral KL(Qhat(dy|z)||Pihat(dy|z)) mathbb Q_(A,o,X)(dz) >= 0
```

On the extended tier, use KL disintegration plus unchanged log evidence without `infinity-infinity`. Prove zero defect iff discarded conditional recognition/posterior laws agree a.s.; state recovery-kernel equivalence only under its hypotheses.

- [ ] **Step 6: Prove holonomy alternatives.**

Keep channels/groupoids separate. Declare joint fine/parent actions, prove `C_A` equivariance and evaluation compatibility, and derive the required covariance or invariance of `\mathbb P_A`, `\boldsymbol\Pi_{A,o,X}`, and `\mathbb Q_{A,o,X}`. Marginal `h_#q_A^x=q_A^x` is insufficient; full triviality is sufficient but not necessary. Alternatively retain root, raw holonomy, and boundary marks in `\mathsf Z_A`.

- [ ] **Step 7: Type but do not solve dynamics.**

For differentiable spaces record `delta_t=partial_t c_t+D c_t V_t-bar V_t o c_t`; for Markov evolution require generator intertwining/lumpability. Mark autonomy, selected membership, Wheelerian feedback, and sustained NEQ `OPEN` with the norm/interval/state-class obligations of later approximate results.

- [ ] **Step 8: Atomize, validate, commit.**

Separate claims for model-family normalization, evaluation compatibility, parent normalization, posterior pushforward, common-channel absolute continuity, projections, VFE chain/equality, holonomy-blind invariance, holonomy retention, and dynamics scope. Make dependencies acyclic. Checkpoint and commit `docs: derive pointwise probabilistic datum`.

### Task 4: Build the Non-Gaussian Witness and Counterexamples

**Files:**
- Create: witness script/output and counterexample proof
- Modify: counterexample register, ledger, DAG, portfolio

**Interfaces:**
- Consumes: Task 3 hypotheses.
- Produces: categorical instance and scoped falsifiers.

- [ ] **Step 1: Implement the categorical witness.**

Use `M=B=E={0,1}` with singleton `Xi_A`, `H_A`, and observation spaces and fixed structural `X`. Let `P(M=m)=1/2`; let the evaluated kernel on `(B,O,H)` satisfy `K_m(B=1)=1/4+m/2`; and add independent fair fine `E`. Recognition keeps the same `(M,B)` posterior marginal but sets `E=B`. `C_A` retains `(B,M)`. Verify exactly:

```text
boldsymbol Pi_(A,o,X)(M,B)=mathbb Q_(A,o,X)(M,B)
mathbb P_A(dB,do,dh|M=m,X)=K_m(dB,do,dh)
q_A^m=q_A^b=Bernoulli(1/2)
KL(mathbb Q_(I,o,X)||boldsymbol Pi_(I,o,X))=log(2); KL(mathbb Q_(A,o,X)||boldsymbol Pi_(A,o,X))=0; Delta_A=log(2)
```

Label it finite categorical, never Gaussian.

- [ ] **Step 2: Prove marginal nonuniqueness.**

Fair correlated support `(0,0),(1,1)` and fair anticorrelated support `(0,1),(1,0)` have identical marginals, distinct joints, and infinite two-way KL.

- [ ] **Step 3: Prove split-channel failure.**

Let fine `Q=Pi` be fair; use identity recognition channel and constant-zero generative/posterior channel. Fine KL is zero; coarse KL is infinite. This refutes unconditional split-channel contraction/VFE identities.

- [ ] **Step 4: Prove evaluation mismatch.**

Reuse `\mathbb P_A` but declare `ev'_A(m)=K_{1-m}`. The model marginal remains normalized while the conditional generative kernel disagrees at every positive-mass `m`; a.s. compatibility repairs it.

- [ ] **Step 5: Prove holonomy boundaries.**

An identity-transport two-node tree with unequal Bernoulli laws has trivial holonomy but no agreement. Bit flip stabilizes the fair law. Correlated/anticorrelated joints have invariant marginals but one-coordinate flip changes the joint.

- [ ] **Step 6: Recompute deterministically.**

Use `Fraction`, symbolic `"log(2)"`, corroborative decimal labels, sorted keys, one LF. Run twice and require equal SHA-256:

```powershell
& 'C:\Python314\python.exe' 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\finite_nongaussian_witness.py'
$first=(Get-FileHash -Algorithm SHA256 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\finite-nongaussian-output.json').Hash
& 'C:\Python314\python.exe' 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\finite_nongaussian_witness.py'
$second=(Get-FileHash -Algorithm SHA256 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\finite-nongaussian-output.json').Hash
if ($first -ne $second) { throw 'nondeterministic finite witness output' }
```

- [ ] **Step 7: Checkpoint and commit.**

Run scripts, JSON/checkpoint/EOL/C0/BOM/diff gates; commit `docs: witness pointwise probabilistic datum`.

### Task 5: Assemble the Rigorous-Theory Release

**Files:**
- Modify: all nine package-root artifacts
- Create: independent reconstruction, oracle erasure, attacks, and review files

**Interfaces:**
- Consumes: Tasks 2-4 evidence.
- Produces: hash-bound static pointwise release.

- [ ] **Step 1: Complete nine mechanism families.**

Include kernel integration, posterior disintegration, model compatibility, KL disintegration, recovery equality, holonomy quotient, holonomy retention, finite falsifiers, and deterministic/stochastic dynamics boundaries. Each needs a failure test; retire recognition-dependent generation routes.

- [ ] **Step 2: Complete atomic ledger/DAG.**

Every ancestor is evidence-verified by derivation/mapped theorem. Counterexample conjuncts use direct counterexample evidence. Dynamics, agency, comparison, and gluing stay outside target closure.

- [ ] **Step 3: Run four independent views.**

Use probability/kernel, information-geometric/VFE, gauge/holonomy, and dynamics/scope reviewers. Give frozen contract/proofs without favored narrative; require exact locations and falsification conditions.

- [ ] **Step 4: Attack all load-bearing seams.**

Attack nonnormalization, observation-dependent channel, recognition-reading generation, null posterior versions, mismatched-channel support, marginal reconstruction, incompatible/nonmeasurable evaluation, kernel quotient regularity, marginal/full holonomy confusion, erased marks, Gaussian leakage, infinite-KL subtraction, and autonomy/ontology overreach. Sustained attacks block affirmation.

- [ ] **Step 5: Reconstruct and erase the prior.**

Re-derive all ancestors from contract/DAG without the direct proof outline. Remove affirmative search prior, scan for paraphrased dependence, and recompute closure. Bind evidence digests.

- [ ] **Step 6: Validate and commit.**

```powershell
& 'C:\Python314\python.exe' 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\notation_scan.py' --registry 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\notation-registry.json' --root . --output 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\notation-collision-report.json'
& 'C:\Python314\python.exe' 'docs\derivations\2026-08-15-full-pointwise-meta-agent\evidence\finite_nongaussian_witness.py'
& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py' --mode release 'docs\derivations\2026-08-15-full-pointwise-meta-agent'
git diff --check
git commit -m "docs: certify pointwise probabilistic datum"
```

Use `COMPLETE_AFFIRMATIVE` only with eligible evidence for every positive conjunct/dependency and every negative counterexample. Otherwise release `INCONCLUSIVE` and do not promote central theory.

### Task 6: Integrate Only Released Claims

**Files:**
- Modify: all canonical integration surfaces listed above

**Interfaces:**
- Consumes: Task 5 release/digest.
- Produces: canonical theorem account and ordered downstream roadmap.

- [ ] **Step 1: Add model evaluation to `03_probability`.**

After structural typing distinguish `q_i^m`, model points, and evaluated kernels; state measurability, noninjectivity, and presentation/quotient boundary. Generation remains independent of recognition.

- [ ] **Step 2: Add posterior pushforward to `06_general_coarsegraining`.**

Beside the evidence-preserving theorem, state the version-qualified posterior identity and test-function proof; cross-reference existing KL chain rule.

- [ ] **Step 3: Add the pointwise probabilistic-datum theorem to `07b_agent_network_rg`.**

In law-level coarse-graining define fine tuple, channel, parent triple, evaluation compatibility, marginals, and defect. State holonomy alternatives near cross-scale operators. Dynamics remains open.

- [ ] **Step 4: Propagate release and exact scope.**

Update SPEC, notation, claim ledger, start guide, overview. Append dated STATUS/worklog sections. Supersede only the marginal-pair boundary. Keep channel/membership selection, autonomy, agency, NEQ, comparison category, patch gluing, limits, physical time, unique physics, and ontology open.

- [ ] **Step 5: Record downstream order.**

1. Comparison theorem: frozen parent experiment with intervention chain `R -> E -> O` and explicit target/boundary/time/relabeling category; interventions remain analyst probes.
2. Patch `\mathcal U_A`: measurable/smooth channels, cocycles, active components, strata, soft multiple membership, holonomy selection, integrable defect; only this phase can construct parent local sections and a geometric meta-agent.
3. Participatory NEQ/emergent agency: one tower action/proved reduction, no double counting, gradient versus open/antisymmetric/kinetic/stochastic/delayed/memory/adaptive mechanisms, operational agency grades.

Mark each `OPEN/TODO`, outside static release ancestry.

- [ ] **Step 6: Build and validate.**

Run release, notation, witness, label/status/UTF-8/C0/BOM/EOL/diff gates. Then:

```powershell
$metaAgentTexOut=Join-Path $env:TEMP 'multiagentelbo-full-pointwise-meta-agent-tex'
New-Item -ItemType Directory -Force -Path $metaAgentTexOut | Out-Null
Push-Location Theory
pdflatex -interaction=nonstopmode -halt-on-error -output-directory $metaAgentTexOut main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory $metaAgentTexOut main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory $metaAgentTexOut main.tex
Pop-Location
rg -n "Undefined control sequence|multiply defined|There were undefined references|Fatal error" "$metaAgentTexOut\main.log"
```

Expected: zero build exits and no matched diagnostics. Do not commit TeX output. Commit `docs: integrate pointwise probabilistic datum`.

### Task 7: Independent Closure and Handoff; Optional Authorized Publication

**Files:**
- Modify only findings-driven Task 2-6 files
- Create: `docs/verification/reviews/2026-08-15-full-pointwise-meta-agent-closure.md`
- Create/update ignored: `.verification/ledger.json`

**Interfaces:**
- Consumes: integrated feature branch.
- Produces: revision-bound closure and downstream handoff; Git publication/parity only after separate authorization.

- [ ] **Step 1: Re-review integrated claims.**

All four domain views check every central status against release. Use `high_severity`, `escalation_target=4`, structured skeptic, and evidence-weighted adjudicator for load-bearing mathematics. Repair Critical/High/Medium findings and repeat affected reviews.

- [ ] **Step 2: Run final gates on exact content commit.**

Re-run release, notation, two-hash witness, three-pass TeX, and static gates. Commit repairs/review and make no tracked edits afterward.

- [ ] **Step 3: Create schema-1.1 closure.**

```powershell
& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.claude\skills\verification\scripts\verification_gate.py' start --cwd . --ledger .verification/ledger.json --mode closure
& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.claude\skills\verification\scripts\verification_gate.py' validate .verification/ledger.json --cwd .
```

One claim per assertion; derivations close mathematics; mechanical results close only mechanical claims. Link four views, skeptic, adjudicator. Drift, absent evidence, or disagreement yields `INCONCLUSIVE`.

- [ ] **Step 4: Stop at the publication authorization gate.**

Do not push, merge, or advance `main` merely because this implementation plan was approved. Report the closure revision and request or confirm separate publication authorization. If separately authorized, fetch and require `origin/main` as ancestor, push without force, fast-forward only a clean authoritative main checkout, rerun the named release/witness gates, push main, fetch, and prove local main, `origin/main`, and `git ls-remote origin refs/heads/main` have identical SHA. Preserve dirty checkouts.

- [ ] **Step 5: Hand off the research map.**

Report theorem, evaluation compatibility, meaning of `Delta_A`, why holonomy does not select membership, governing files/SHA, and three downstream projects. Offer wiki ingest; do not write without approval.

## Deferred Project Boundaries

This plan ends with the full static probabilistic datum at one $r_*$. It does not yet construct a
pair of parent local sections or a full geometric meta-agent. Separate future proof programs cover:

- comparison category: the released parent experiment with `R -> E -> O` plus frozen morphisms;
- patchwise `\mathcal U_A`: gluing `r\mapsto C_{A,r}`, bundle transitions, stratified active sets,
  retained holonomy, and an integrable defect; and
- participatory nonequilibrium: one coupled dynamics, factor counting, semiconjugacy/lumpability,
  typed NEQ mechanisms, and operational agency criteria.

No present result may be cited as closing these boundaries. Publication also remains a separate
authorization after revision-bound closure.
