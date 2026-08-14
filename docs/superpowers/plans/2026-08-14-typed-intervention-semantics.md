# Typed-Intervention Semantics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove and publish a finite passive-to-interventional nonidentifiability theorem that survives null-node reduction and does not depend on node-count bookkeeping.

**Architecture:** A rigorous-theory-search package freezes a universal passive-identifiability target, an exact `Fraction` witness supplies executable controls, and direct proofs define raw typed presentations plus their operational response reduction. Central theory receives only the released finite theorem and preserves the ontology/continuum boundaries.

**Tech Stack:** Python 3.14 standard library (`fractions`, `itertools`, `json`), pytest, LaTeX/pdflatex, rigorous-theory-search validator, verification schema 1.1, Git worktrees.

**Spec:** `docs/superpowers/specs/2026-08-14-typed-intervention-semantics-design.md`

## Global Constraints

- Work only in `C:\Users\chris and christine\Desktop\MultiAgentELBO\.superpowers\worktrees\MultiAgentELBO-typed-intervention-semantics-20260814` on `codex/typed-intervention-semantics-20260814`, based on `origin/main` at `f956c7f1d7fb035d157b415c670a13a46f631233`.
- Use American English in every added or edited line.
- Use `C:\Python314\python.exe` for every CPU test and validator command; set `CUDA_VISIBLE_DEVICES=-1` and `PYTHONHASHSEED=0` for full-suite evidence.
- Commit this approved design and plan before Task 1 so every later artifact is revision-bound to an explicit input.
- Follow strict TDD for the exact witness: persist an observed failing RED before creating production witness code.
- Use `Fraction` for all probability, channel, intervention, and total-variation calculations. Floating-point probability calculations are forbidden.
- The load-bearing counterexample is the same-signature pair `(a,b)=(1/4,1/3)` and `(1/3,1/4)`, with passive crossover `5/12` and a full reduced-response image in `L_1` that is absent from `L_2` under every admitted boundary relabeling. Contrasts `1/3` and `1/2` are diagnostics only.
- The direct/split/null witness is a control, not the negative certificate. Its parameters are `a=1/10`, `b=1/8`, direct crossover `1/5`, and null probability `eta=2/5`.
- Operational reduction uses the total right-override partial-assignment monoid and equality of complete two-sided response signatures. It must collapse the independent null node.
- Theorem statements use `Red : FinTIP -> FinRIE` and `Ubar_pass : FinRIE -> FinObs`. The theorem refutes universal two-sided recovery `R Ubar_pass ~= identity`; it does not refute a conventional right inverse `Ubar_pass R ~= identity`.
- Do not identify a mediator, null node, intervention target, or reduced protocol class with autonomous agency or physical ontology.
- Keep the August 13 and existing August 14 theorem packages byte-unchanged.
- New package text and `tests/test_typed_intervention_semantics_witness.py` use LF through exact path-specific `.gitattributes` rules; the six central theory/status files retain CRLF.
- Tasks 1-5 are sequential writers. Task 3 owns its four files through its commit; Task 4 starts only after that commit. Task 6 starts only after every writer is idle and assigns any findings-driven repair to one owner at a time.
- Every mathematical closure claim requires a direct derivation. Exact execution corroborates but does not prove the theorem.
- No release or publication claim is valid until the release validator, exact tests, independent reviews, full CPU suite, TeX build, and closure ledger pass on the exact final commit.

---

### Task 1: Scaffold the frozen run and establish exact-witness RED

**Files:**
- Modify: `.gitattributes`
- Create: `docs/derivations/2026-08-14-typed-intervention-nonidentifiability/**`
- Create: `tests/test_typed_intervention_semantics_witness.py`

**Interfaces:**
- Consumes: the approved design and rigorous-theory-search templates.
- Produces: a digest-bound checkpoint package, exact witness test contract, durable failing JUnit file, test snapshot, and TDD record.

- [ ] Add exact `text eol=lf` rules for both `docs/derivations/2026-08-14-typed-intervention-nonidentifiability/**` and `tests/test_typed_intervention_semantics_witness.py`.
- [ ] Scaffold the run with `& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\scaffold_run.py' --date 2026-08-14 --slug typed-intervention-nonidentifiability 'docs\derivations'`.
- [ ] Freeze the universal target with `quantifier_class=UNIVERSAL` and `negative_certificate_kind=COUNTEREXAMPLE`; bind every artifact to the canonical target digest and record the committed design/plan revision.
- [ ] Write `tests/test_typed_intervention_semantics_witness.py` first. Freeze every signature, exact table, validation error, two-sided response image, relabeling control, and deterministic JSON requirement from the spec. Its loader must fail every test only because the witness file is absent.
- [ ] Run `C:\Python314\python.exe -m pytest tests\test_typed_intervention_semantics_witness.py -q --basetemp=C:\tmp\maelbo-typed-intervention-red-20260814 --junitxml=docs\derivations\2026-08-14-typed-intervention-nonidentifiability\evidence\red-junit.xml`; require every collected test to fail for the declared absent-witness reason.
- [ ] Normalize the RED XML to LF and strip only trailing whitespace; snapshot the LF test byte-identically; record the command, totals, raw SHA-256, filtered Git blob identity, and failure reason in `evidence/tdd-record.md`.
- [ ] Run `& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py' --mode checkpoint 'docs\derivations\2026-08-14-typed-intervention-nonidentifiability'`, `git diff --check`, C0/CR/BOM scans, and `git ls-files --eol`; commit `test: freeze typed intervention witness contract`.

### Task 2: Implement the exact witness and reach GREEN

**Files:**
- Create: `docs/derivations/2026-08-14-typed-intervention-nonidentifiability/evidence/exact_typed_intervention_witness.py`
- Create/modify: package GREEN JUnit and TDD evidence files

**Interfaces:**
- Consumes: Task 1's exact test API and hand-derived fixtures.
- Produces: exact normalized laws, intervention responses, operational signatures, same-signature counterexample data, and deterministic JSON.

- [ ] Implement the frozen API exactly, including immutable `Fraction` tuples, lexicographic state ordering, canonical context tuples, total right override, model-specific node validation, and every required `ValueError`.
- [ ] Implement the nine frozen shared retained-signature tables literally and verify the control passive table `(2/5,1/10,1/10,2/5)`.
- [ ] Implement complete two-sided contextual signatures and canonical quotient-monoid response images; keep raw structural invariants separate.
- [ ] Exhaustively verify both null assignments against all 27 partial `{R,E,O}` contexts and construct the forget-`N` reduced-monoid isomorphism.
- [ ] Make `same_signature_counterexample` return exact passive equality, the frozen mediator responses and diagnostic contrasts, fifteen behavioral classes per model, and the unmatched full response-image certificate under all four boundary relabelings.
- [ ] Make `main()` print the exact four-key recursively transformed summary from the spec: booleans and categorical strings are preserved, every numeric value becomes a reduced rational/decimal string, keys are recursively sorted, separators are compact, and there is exactly one terminal LF. Compare two in-process and one fresh-process byte stream.
- [ ] Run the focused GREEN command from Task 1 and persist LF JUnit with zero failures/errors/skips.
- [ ] Mutation-test wrong channel composition, ignored `b`, omitted left/right context composition, an altered response-image entry, collapsed class multiplication, equalized contrasts, and unsorted nested JSON. For every mutant retain command, failing test/JUnit, exit status, and pre/post SHA-256; restore production source byte-identically.
- [ ] Check raw/filtered Git blob identity for the witness, test, snapshot, and JUnit; run `& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py' --mode checkpoint 'docs\derivations\2026-08-14-typed-intervention-nonidentifiability'`, C0/EOL scans, and `git diff --check`; commit `test: add exact typed intervention witness`.

### Task 3: Prove the raw category and operational reduction theorems

**Files:**
- Create: `evidence/typed-category-proof.md`
- Create: `evidence/operational-reduction-proof.md`
- Modify: `construction-or-strongest-theorem.md`
- Modify: `counterexample-register.md`

**Interfaces:**
- Consumes: the frozen contract and exact witness controls.
- Produces: direct derivations for groupoid well-definedness, passive equality, contextual reduction, same-signature reduced nonisomorphism, and no-two-sided-recovery.

- [ ] Exclusively own `evidence/typed-category-proof.md`, `evidence/operational-reduction-proof.md`, `construction-or-strongest-theorem.md`, and `counterexample-register.md` until this task commits; Task 4 must not edit them concurrently.
- [ ] Prove normalization by finite DAG factorization, hard-intervention closure, typed-isomorphism transport, and functoriality of `Red`.
- [ ] Prove the right-override partial-assignment operation is a monoid and that equality of complete two-sided response signatures is an equivalence and a two-sided congruence; derive the quotient monoid and descended response map.
- [ ] Prove exhaustively that the independent null extension is behaviorally null under both assignments and all 27 retained/mediator/record contexts, and that forgetting `N` induces the split/null quotient-monoid isomorphism.
- [ ] Prove same-signature passive equality; retain `abs(1-2b)` only as a diagnostic; use the exact unmatched `L_1` response law across the complete `L_2` response image and all four typed boundary relabelings as the negative certificate.
- [ ] Prove nonessential injectivity of `Ubar_pass` and the no-`R Ubar_pass ~= identity` corollary; preserve the `Ubar_pass R ~= identity` allowance and ontology boundary.
- [ ] Run `& 'C:\Python314\python.exe' -m pytest 'tests\test_typed_intervention_semantics_witness.py' -q`, `& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py' --mode checkpoint 'docs\derivations\2026-08-14-typed-intervention-nonidentifiability'`, C0/prior-leak/EOL scans, and `git diff --check`; commit `docs: prove typed intervention nonidentifiability` before Task 4 begins.

### Task 4: Assemble and release the rigorous-theory certificate

**Files:**
- Modify: `problem-contract.json`
- Modify: `claim-ledger.json`
- Modify: `dependency-dag.json`
- Modify: `approach-registry.json`
- Modify: `adversarial-report.json`
- Modify: `release.json`
- Modify: `construction-or-strongest-theorem.md`
- Modify: `counterexample-register.md`
- Modify: `final-report.md`
- Create: `evidence/independent-reconstruction.md`
- Create: `evidence/oracle-erasure.md`
- Create: `evidence/adversarial-attacks.md`

**Interfaces:**
- Consumes: Tasks 1-3 proofs, exact evidence, and frozen digest.
- Produces: a hash-bound `COMPLETE_NEGATIVE` release with no candidate ancestor.

- [ ] Start only from Task 3's committed revision. Take exclusive ownership of the whole new package and do not modify any prior August 13/14 package.
- [ ] Populate atomic claims and an acyclic DAG; the target closure depends on passive equality, the exact unmatched response-image invariant under all boundary relabelings, and reduced nonisomorphism; not on TV alone or null-node inventory.
- [ ] Populate mechanism families for raw syntax, the right-override action monoid, two-sided congruence, retained quotient, same-signature response image, direct/split/null control, reduced forgetful-fiber proof, conventional section, and minimal-realization future work.
- [ ] Independently reconstruct the definitions, all exact tables, the fifteen-class enumeration, and the counterexample from the frozen contract.
- [ ] Attack category dependence, protocol-monoid automorphisms, abstract-action simulation, null deletion, boundary relabeling, response-set matching, right-inverse confusion, normalization, conditioning-null events, and agency overreach.
- [ ] Run semantic oracle erasure; bind every contained source/evidence/TDD hash; set `terminal_status=COMPLETE_NEGATIVE`; use the exact final-report headings; run `& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.agents\skills\rigorous-theory-search\scripts\validate_run.py' --mode release 'docs\derivations\2026-08-14-typed-intervention-nonidentifiability'`, an independent hash audit, EOL/C0/BOM scans, and `git diff --check`; commit `docs: certify typed intervention nonidentifiability`.

### Task 5: Integrate the certified finite boundary into central theory

**Files:**
- Modify: `Theory/05d_relational_inference.tex`
- Modify: `Theory/SPEC.md`
- Modify: `Theory/appendix_claim_ledger.tex`
- Modify: `overview.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md`

**Interfaces:**
- Consumes: Task 4's release-validated certificate.
- Produces: a consistent central account of the declared category, reduction, same-signature no-go, and remaining ontology boundaries.

- [ ] Define the raw groupoid, right-override action monoid, two-sided behavioral congruence, `Red`, `Ubar_pass`, same-signature response-image theorem, null-collapse control, and no-two-sided-recovery corollary adjacent to the current intervention open problem in `05d`, using collision-free labels.
- [ ] Update SPEC, overview, and appendix only at the finite declared-category scope. Preserve category-independent and ontological uncertainty, and state that mediator TV is diagnostic rather than the proof invariant.
- [ ] Append dated STATUS and worklog entries without rewriting earlier chronology; include the target digest, exact category, reduced-functor typing, and response-image boundary.
- [ ] Run `& 'C:\Python314\python.exe' -m pytest 'tests\test_typed_intervention_semantics_witness.py' -q`, the exact release-validator command from Task 4, and label/C0/UTF-8/EOL/American-English scans. Run `New-Item -ItemType Directory -Force 'C:\tmp\maelbo-typed-intervention-tex-20260814'`, then three `pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory='C:\tmp\maelbo-typed-intervention-tex-20260814' main.tex` passes from `Theory`; run `git diff --check`.
- [ ] Commit `docs: integrate typed intervention semantics`.

### Task 6: Perform independent closure, final verification, and publication

**Files:**
- Modify only findings-driven Task 1-5 files.
- Create/update ignored `.verification/ledger.json` for the exact final revision.

**Interfaces:**
- Consumes: the complete feature branch.
- Produces: independent approval, exact final evidence, validated closure ledger, and published refs.

- [ ] Wait until every Task 1-5 writer is idle, then dispatch independent category/proof, exact-witness, adversarial equivalence/ontology, and manuscript-boundary reviewers in parallel. Give findings only to the coordinator; assign each repair round to one exclusive fix owner and re-review every Critical/Important/Medium correctness finding.
- [ ] On the final content commit, rerun the exact focused and release commands above, then run `$env:CUDA_VISIBLE_DEVICES='-1'; $env:PYTHONHASHSEED='0'; & 'C:\Python314\python.exe' -m pytest -q --junitxml='C:\tmp\maelbo-typed-intervention-final-20260814.xml'`. Read totals from that XML. Rerun the exact three-pass TeX command, independent evidence-hash/EOL/C0/UTF-8/label audits, and `git diff --check`.
- [ ] Start closure with `& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.claude\skills\verification\scripts\verification_gate.py' start --cwd '.' --ledger '.verification\ledger.json' --mode closure`; populate the schema-1.1 ledger bound to that exact commit with two mathematics views, code/evidence views, adjudication, and skeptic linkage; then run `& 'C:\Python314\python.exe' 'C:\Users\chris and christine\.claude\skills\verification\scripts\verification_gate.py' validate '.verification\ledger.json' --cwd '.'`. Any post-ledger source edit invalidates closure and requires a fresh restart/rebind.
- [ ] Fetch and require `origin/main` as branch ancestor; explicitly push the feature. In the clean real checkout, fetch, require `main == origin/main`, merge `--ff-only`, rerun focused/release checks, push `main` without force, fetch, and prove local main, `origin/main`, and `git ls-remote` are byte-identical SHAs.
- [ ] Preserve the worktree and branch. Report exact SHAs and machine-readable JUnit totals, and offer Research-wiki ingest without performing it until separately confirmed.
