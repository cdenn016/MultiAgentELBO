# Ultradeep peer review of `Theory/` — Wave-3 adjudication log

Running record of the adversarial pass. Each entry is a finding from the interim report or a
resumed lens, plus the verdict of the skeptic dispatched against it and the corrected statement
that survives. A finding is not reportable until it appears here with a verdict.

Companion to `2026-08-09-ultradeep-peer-review-INTERIM.md`.

## V1 — missing check behind two load-bearing claims

**Original (critical):** "Two of three load-bearing numerical claims have no executed evidence."
`claims.json` declares 30 checks, `current-results.json` holds 29, and the missing
`CHK-CG-FACTOR-GAP-STRESS-3138` is the sole check behind `NUM-CG-FACTOR-GAP-STRESS-SCHEDULE`
(`appendix_numerical_provenance.tex:71`) and `NUM-CG-FACTOR-GAP-BOUNDARY-PROTOCOL` (`:128`).

**Verdict: PARTIALLY CONFIRMED. Critical downgraded to medium.** The 29-vs-30 gap is real. Every
inference drawn from it is not.

The manuscript discloses the gap in print, in the same appendix, thirty lines below the evidence
the finding quoted. `appendix_numerical_provenance.tex:147-150`: "The checked-in
`verification/current-results.json` is the older 29-check artifact. It is not evidence for this
30-check package. A governed 30-check regeneration remains required before that evidence is
current. This appendix does not claim that deferred artifact is current." Mirrored at
`VERIFICATION.md:69-73`. Concealment is the predicate for critical and it is absent — the finding's
own sentence "has never been recorded as run in any committed artifact" paraphrases the
manuscript's closing paragraph.

The "two of three" partition is wrong. By `:147-150` the stale artifact is not evidence for any of
the thirty checks, including `CHK-GAUSS-CONDITIONING`, which the finding credited as the one
load-bearing claim with evidence. This is one package-level freshness statement, already made, not
two per-claim evidence gaps.

Nothing depends on it. A grep for `3138`, `FACTOR-GAP-STRESS`, and "factorization-gap stress" across
`Theory/*.tex` returns six hits, all inside `appendix_numerical_provenance.tex`, and zero across the
twenty-two body chapters. Per `claims.json:69` and `:86` the two claims assert (a) the check's own
PASS criterion and (b) which fields `GapStep` and `FactorizationCaseRecord` serialize, together with
the disclaimer that `backward_error_bound` "is not a certified perturbation or forward-error bound."
The second is substantially a list of things the package declines to assert.

The check exists, runs, and reproduces. Executed: `check_cg_factor_gap_stress()` returns PASS in
12.7 s, with `finite_values = 3138`, `all_case_oracle_attempts = 3138`, `oracle_failures = 0`, and
the boundary witness at `rho_squared_excursion = 4.44e-16` inside `outward_allowance = 9.43e-16`.
All eight strata of the table at `:51-58` reproduce bit-for-bit. The distance between the manuscript
and the record is twelve seconds of CPU, not a missing experiment.

The runner fails closed. `run_checks.py --verify current-results.json` returns
`{"ok": false, "issues": [{"code": "MISSING_GOVERNED_PATH"}], "published_result_sha256": null}` with
exit 1, and the strict-zip roster gate at `:8496` raises on the 29/30 mismatch rather than
admitting it. `VERIFICATION.md:63-67` tells consumers to require `ok=true`; they get `ok=false`.
This also revises V8: the artifact indeed cannot be re-verified, but the failure is safe, not silent.

**What survives.** `claims.json:78` and `:95` record `missing_obligation: null` for both claims
while the prose says regeneration remains required, so the machine-readable inventory under-records
what the text discloses. Weak on its own, since all thirteen entries carry `null` and the field
therefore discriminates nothing. Second, `appendix_numerical_provenance.tex:28-30` names the JSON
record "the authority for exact counts and numerical values" and disclaims duplicating drift-prone
result tables, while `:45-62` prints a 17-digit table whose nominated authority does not currently
contain the check. This is the same defect V2 isolates, reached from the other side. Third and
cosmetic, `check_cg_factor_gap_stress()` returns `claim_ids = ['NUM-CG-FACTOR-GAP-BOUNDARY-PROTOCOL']`
alone while `claims.json:76` and `:93` map both claims to it; the validator gates claims-to-checks
at `:7067`, so nothing breaks.

**Retracted:** the charge that `VERIFICATION.md` describes a package the artifact cannot instantiate
is wrong on the specific sentences cited. `:320` "The suite contains 30 deterministic checks" is
true — `PRODUCTION_CHECK_IDS` at `run_checks.py:5727` has exactly 30 entries with the stress check at
index 18. `:221-222` "PASS requires all 31 ordered checks" is a requirement on a production result,
true against `PRODUCTION_REQUIRED_CHECK_IDS` at `:5759`. Neither is a statement about the
checked-in artifact, whose status is given separately and correctly at `:69-73`. Three statements
about three different objects, all accurate. V8 needs rewriting to the one inconsistency that holds.

**Falsification conditions:** a body chapter citing the 3,138 protocol in support of a proposition;
any sentence asserting in the present indicative that the 30-check run was executed and recorded;
or `check_cg_factor_gap_stress()` returning non-PASS on a clean-room checkout at the governed vault
path with pinned NumPy 2.4.4 / SciPy 1.17.1 / mpmath 1.3.0.

### Second skeptic, independent angle: mechanics

A second skeptic attacked the same finding on existence rather than severity and reached the same
verdict, which makes the downgrade a majority result rather than one reviewer's judgment.

Every mechanical assertion reproduces, and each escape route in the brief was closed. The union is
exactly 30 with no double-count: 20 `supplemental_check_ids` plus 11 distinct ids across 13
`claims[].check_ids`, overlapping in exactly one element, the stress check itself. Results are 29,
`set(declared) - set(results) = ['CHK-CG-FACTOR-GAP-STRESS-3138']` and the reverse is empty. No
id-remapping table exists; both occurrences of the id in `run_checks.py` are canonical. Both claims
carry that single check id and nothing else, and exactly three claims are `load_bearing: true`. The
check is unconditional at index 17 of `CHECKS` — no environment variable, no tier, no slow marker —
and appears in both `PRODUCTION_CHECK_IDS` and `PRODUCTION_REQUIRED_CHECK_IDS`. Re-executed at
14.7 s with byte-identical `case_payload_digest` across two runs, confirming determinism, and the
strata reproduce `appendix_numerical_provenance.tex:35-37` exactly.

**The surviving defect, sharpened.** The artifact carries no in-band staleness marker. Grepping the
raw JSON returns zero hits for `stale`, `superseded`, or `not evidence`, while `overall_status: PASS`
and `mapping_validation.status: PASS` sit at top level. `claims.json` compounds it with
`current_protocol_reproducible: true` and `recommended_disposition: keep_exact` on both claims. A
human who reads `VERIFICATION.md` is correctly warned; a machine consumer reading only the JSON is
misled. That is the defect to report, and it is cleanly fixable with an in-band
`status: HISTORICAL` field.

**Root cause, which reframes V1 as a symptom.** This is not a run that skipped one check. Of the 24
manifest-bound TeX sources, 23 mismatch; `appendix_numerical_provenance.tex` is 2,089 bytes in the
manifest against 8,824 on disk, so the text at `:71` and `:128` did not exist when the artifact was
produced. The artifact records 11 `claim_dispositions` against 13 claims and 19 supplemental ids
against 20. It predates the current manuscript wholesale. None of the committed results are evidence
for any current claim, not merely the two factorization-gap ones. V1, the stale half of V2, V3, and
V8 are therefore one defect seen from four directions, and the report should merge them.

**Confirmed independently by both skeptics:** `run_checks.py:4988` emits
`claim_ids: ["NUM-CG-FACTOR-GAP-BOUNDARY-PROTOCOL"]` alone, so even a regenerated 30-check artifact
would leave `NUM-CG-FACTOR-GAP-STRESS-SCHEDULE` unnamed by any check's `claim_ids`.

## V4 — `CHK-RG-NONCOMMUTING-FLOATING` cannot fail

**Original (high):** the check solves the pencil `(bar, bar)`, whose spectrum is identically one for
any SPD `bar`, so it is structurally incapable of failing and measures LAPACK roundoff.

**Verdict: PARTIALLY CONFIRMED. High downgraded to low.**

The headline is false and mutation testing shows it. `bar` is SPD only because
`positive_quotient_basis` (`run_checks.py:5393-5397`) strips the kernel at a relative `1e-10` cut.
Break that and the check fails. Six mutants, three killed:

    kernel retained (mask eig > -tol)        LinAlgError  -> FAIL
    unfiltered full eigenbasis               LinAlgError  -> FAIL
    lap sign flipped                         ValueError   -> FAIL
    q = random orthonormal, unrelated to lap  PASS  err 3.997e-15
    lap = arbitrary SPD, not a Laplacian      PASS  err 1.665e-15
    lap = identity                            PASS  err 0.0

The raises do not escape as crashes: `:8423-8443` records `status: FAIL` with
`evidence_kind: mechanical_failure`, and `:8461-8473` propagates a failing supplemental id into
`CHK-SOURCE-INVENTORY`. Nor is the gate tolerance-vacuous — the pencil error grows with
conditioning, measured at n=12: `cond 1e6 -> 2.95e-11` PASS, `cond 1e8 -> 1.62e-09` FAIL,
`cond 1e12 -> 1.24e-05` FAIL.

**What survives.** The three passing mutants establish that the check carries no noncommuting-limit
content: it passes with `lap` replaced by the identity. Its real predicate is that the quotient
restriction is positive definite and conditioned better than roughly `1e7`. Its title, "Seeded
six-agent floating quotient-pencil control," and its `expected` field at `:5472`,
"quotient_generalized_eigenvalues: within tolerance of one," both present an exact-arithmetic
identity as a prediction. That is a labeling defect.

Severity falls to low because nothing rests on it. A repo-wide grep for `CHK-RG-NONCOMMUTING`
returns zero hits in any `.tex`, in a manuscript that does cite checks by name elsewhere
(`06_gaussian.tex:294`, `:349`, `:351`, `07_restrictions.tex:298`, `08_infogeometry.tex:195`). No
`claims.json` entry lists it. The manuscript's noncommuting content is analytic, not numerical:
`10_renormalization.tex:395-401` gives the iterated limits in closed form with no NUMERICAL tag, and
`prop:rg-noncommuting-limits` at `07_general_renormalization.tex:882` is a proposition.

**Adjacent finding worth its own line (N2, low).** `positive_quotient_basis:5395` admits
`cond(bar)` up to `1e10`, which is inside the band where the `1e-10` pencil gate fails. The filter
and the gate are not consistent with each other; an admissible input near the filter's edge would
fail the check for a reason unrelated to any defect.

**Credit, and it belongs in the ledger.** The two sibling checks covering the same theory both
discriminate under mutation. `check_rg_noncommuting_limits_symbolic:5400-5452`: perturbing the
two-node Laplacian yields `d²ε²+3d²ε+d²-3dε-2d+1` against the expected `d·ε·(dε+2d-2)`, mutant
killed. `check_rg_mass_pencil:5484-5518` uses an independent SPD reference form at `:5488` and tests
the nontrivial law `d_k = λ_k/(λ_k+a)`: true law `1.33e-15` PASS; `λ/(λ+2a)` `1.72e-01` FAIL;
`1/(λ+a)` `1.11e+00` FAIL; reference replaced by identity `5.69e-01` FAIL. Three killed by nine to
ten orders above the gate. The discriminating pencil work is done at `:5484`, and the original
finding's proposed fix — match the sibling pattern — is the right one.

**On the "mandatory" charge.** `VERIFICATION.md:332-334` scopes "mandatory" to must-run-and-pass,
and `:337-343` states that PASS "does not prove a theorem, genericity, convergence, universality,
blocking-scheme independence, or a physical law." The roster is internal to the verification
package; no `.tex` mentions it.

## P1 — epistemic structural realism mis-tagged and mis-cited

**Original (high):** the manuscript's one positive interpretive conclusion, at
`12_philosophy.tex:183-187`, is tagged DEFINITION while asserting an evidential relation; it escapes
the OPEN fence both neighbouring readings receive; and it cites Worrall 1989, whose argument is
diachronic, for a synchronic invariance list, which is gauge redundancy.

**Verdict: LARGELY REFUTED. High downgraded to low.** Sub-claims (3) and (4), the load-bearing
ones, are false. This is the finding the adversarial pass existed to catch.

**The Worrall citation is used correctly (sub-claim 3, refuted).** The skeptic obtained the full
text and calibrated pagination against SEP's two citations, establishing a reprint-to-Dialectica
offset of exactly 40. Worrall's final section applies structural realism synchronically, to a single
currently-accepted theory with no successor, warranted by empirical success rather than by theory
change. Dialectica 122-123: "Is there any reason why a similar structural realist attitude cannot be
adopted towards quantum mechanics? ... The structural realist simply asserts, in other words, that,
in view of the theory's enormous empirical success, the structure of the universe is (probably)
something like quantum-mechanical." No Fresnel, no Maxwell, no succession. Dialectica 122 on Newton:
"what Newton really discovered are the relationships between phenomena expressed in the mathematical
equations of his theory." The Poincaré passage Worrall endorses at Dialectica 118 is likewise an
unrestricted epistemic thesis: "The true relations between these real objects are the only reality
we can attain." Fresnel/Maxwell is Worrall's evidence that the epistemic thesis is livable; the
thesis itself is the form/content distinction, stated and applied without a successor theory. The
manuscript's phrase "in Worrall's sense" picks out exactly that thesis, and epistemic structural
realism is the standard label for it.

The finding's supporting gloss is also self-undermining. "Gauge redundancy licenses less commitment
to the redundant coordinates, not more" — less commitment to frame-dependent representatives and
commitment only to what survives reframing is the epistemic-SR conclusion. The finding states ESR
and labels it a refutation of ESR.

**The holonomy objection is refuted on two independent errors (sub-claim 4).** First, wrong
holonomy. `12_philosophy.tex:92-96` types the data classes, and `eq:phil-holonomy` at `:99-106`
defines `H_γ^b` as the graph-link product `Θ^b_{e_0} Θ^b_{e_1} ... Θ^b_{e_{r-1}}`. The superscripts
`b` and `m` are belief and model sector, not base. The concession the finding leaned on at
`:154-155` concerns base holonomy built from `Ω_γ`, a different object the chapter distinguishes
three separate times (`:122-126`, `:313-314`, `:342-343`). The objection collapses on a superscript.
Second, the idle-wheel criterion says the opposite of what the finding reported. `:114-120` applies
it only to the flat specialization, and states that "A declared nontrivial graph-link holonomy
supplies a model-internal referent"; `:305-306` restates the class as non-idle; `:320-323` makes it
computable. The NOT-CLAIMED at `:112` denies a different inference — evidence of base curvature or
bundle topology — not the invariance.

**The asymmetry exists but is principled (sub-claim 2, partially confirmed).** Four fences the
finding did not quote: `:183` scopes the invariants "on the exact domains established earlier";
`:185-187`, inside the same block immediately after the sentence at issue, says the brackets denote
passive-coordinate equivalence classes "not connection-independent canonical geometries"; `:212-213`
states "The manuscript does not claim that either structural reading follows from its invariance
results" under NOT-CLAIMED; and the chapter's closing line at `:342-343` requires a viable
interpretation to distinguish graph-link holonomy, base-connection holonomy, bundle topology, and
gauge redundancy — the finding's own objection, raised by the chapter itself. The asymmetry is also
motivated by a stated logical difference rather than by preference: `:194-196` and `:208-210` name
the additional bridge premise each fenced reading needs and epistemic SR does not.

**The tag mechanism is refuted, but a real inconsistency survives (sub-claim 1).** DEFINITION
promises "nothing is being proved and the text says so." Nothing is proved in the block, and
`12_philosophy.tex:4` says so. The chapter's own convention at `:6` makes reading-declarations
DEFINITION. The skeptic also closed the escape route it was handed, reporting against its own case
that the chapter never defines epistemic structural realism as a term of art.

**What survives, and it is the whole of P1.** The chapter runs an explicit template twice for
importing a cited philosophical position — `:82-86` for constructive empiricism and `:198-202` for
moderate SR — each with a "this is a declared use of the cited position, not a theorem of the
manuscript" disclaimer. The Worrall sentence gets neither the "denotes" clause nor the disclaimer.
That is a missing eleven-word clause in a chapter that proves nothing. Fix: split the sentence into
its own block and append the standard disclaimer, or write "is read as" in place of "supports."
Optional second item: Worrall's synchronic warrant is a theory's empirical success, which the
chapter concedes it lacks at `:340-341`; a cross-reference from `:184` to that admission would close
the loop.

**Blast radius: none.** `Worrall`, `structural realis`, and `I_struct` occur in `12_philosophy.tex`
only, with zero hits in `appendix_claim_ledger.tex` and no downstream consumer.

**Recorded as adjudicated-not-a-defect:** the Worrall attribution, and the holonomy membership of
`[H_γ^b]_conj` in `eq:phil-invariants`. Neither should be re-raised in a future pass.

## P4 — interpretation chapter cites only the obstruction that helps it

**Original (high):** `12_philosophy.tex` makes exactly five cross-references, the only
obstruction-chapter result among them is `thm:obs-agent-interaction-equivalence` — the one
supporting the participatory reading — and three that constrain it are absent. A reader of chapter
12 alone takes the self-constituting-prior reading as unsupported rather than as proved impossible.

**Verdict: REFUTED at high. Downgraded to low, editorial.**

**The premise fails at the root.** `thm:obs-agent-interaction-equivalence` is not an
obstruction-chapter result. It is defined at `05b_local_collective_elbo.tex:721`, inside the section
"Are observations only agent-agent interactions?" in the chapter Local and Collective Free Energy,
which `main.tex:129` places seventh — four chapters before `11_obstructions`. A repo-wide grep
returns exactly two hits, the definition at `05b:721` and the use at `12_philosophy.tex:259`, and
zero hits in `11_obstructions.tex`.

The `obs-` prefix is overloaded across two namespaces: 78 `obs-` labels in
`05b_local_collective_elbo.tex` where it abbreviates "observation", and 75 in `11_obstructions.tex`
where it abbreviates "obstructions". This is the third finding in this pass to fail by reading a
symbol as provenance when it encoded subject matter, after the `b`/`m` superscripts in P1. The
consequence is structural, not incidental: the finding's shape is "cites the one that helps, omits
three that constrain," and chapter 12 cites zero chapter-11 results by macro. There is no selection
pattern to indict. The treatment is uniform and prose-only, consistent with `:4`.

**Four independent supporting refutations.** The cross-reference count is six, not five (`:40`,
`:52`, `:144`, `:148`, `:259`, `:295`). The one theorem cited carries its own counterweight and
chapter 12 imports it — `05b:743-747` states the theorem "does not eliminate the conditioning role,"
and `12_philosophy.tex:264` restates that as the first item of its NOT-CLAIMED list. The obstruction
content is present in prose, which the finding's own framing concedes discharges the duty: `:268-271`
paraphrases `11_obstructions.tex:250`, the sentence that itself cites
`prop:obs-declared-root-unavoidable`, and `:280-282` declines the strong form. `eq:obs-tension`
appears in substance at `:305-311` marked OPEN, tracking `11_obstructions.tex:393` and `:413-418`.
The two remaining results are scoped away: `cor:obs-flat-fold-singular` rejects "only one flat
unanchored reciprocal Gaussian potential" (`11:254`) while chapter 12 invokes the proper Gaussian-star
model, which `11:404` says avoids the incompatibility; `prop:obs-normalizer-link-dependence` is
fenced at `11:154` as not proving a force along a gauge orbit, and chapter 12 makes no such claim.

**The cherry-picking charge inverts.** `11_obstructions.tex:237` states the role of
`prop:obs-declared-root-unavoidable` explicitly: "That a prior must be declared somewhere is not a
shortcoming of this particular construction, and it is worth recording as a general fact rather than
as a concession." It constrains every finite acyclic generative model equally.

**The load-bearing sentence assumes a claim chapter 12 never makes.** `:288-291` marks strong
agent-only ontology NOT-CLAIMED; `:300` states ontological closure "is not claimed"; `:273-274` says
the Wheeler resemblance "is neither derived from nor evidence for it." Marking NOT-CLAIMED something
later proved impossible under-states the manuscript's own strength. That is the opposite of the
overreach a high finding requires.

**What survives:** `12_philosophy.tex:270` could add `\Cref{prop:obs-declared-root-unavoidable}` to
the sentence attributing the placement of the participatory loop, upgrading a prose attribution to a
pointer. One macro.

**New finding surfaced during the attack (N3, medium — a genuine proof gap).** Verified directly by
the synthesizing reviewer against `11_obstructions.tex:239-243`, and the precise form is sharper
than the skeptic stated.

`prop:obs-declared-root-unavoidable` makes two assertions in one sentence at `:240`. First, "In any
finite directed acyclic generative model there is at least one latent with no parents, whose
marginal law is therefore part of the declared parameters." Second, "Hence no finite acyclic
construction can have every prior constituted by other latents." Tagged ESTABLISHED. The whole proof
at `:243` reads: "A finite directed acyclic graph admits a topological order, and its first element
has no incoming edges. Its factor in the joint is unconditional, so it is declared."

The proof establishes a property of the topologically first *node*. Nothing makes that node latent.
This is not a hypothetical gap in this manuscript: `01_introduction.tex:38` fixes the generative
joint as `P_θ(do, dY | X)`, conditioned on a design `X`, so observed exogenous variables are present
by construction and a latent in `Y` may well have a parent in `X`. The topologically first node of
the full graph is then typically an element of `X`, not a latent.

The two assertions come apart under repair. Restricting the topological order to the induced
subgraph on latents — itself a finite DAG — yields a latent with no *latent* parents. That is enough
for the second assertion, which is the one everything downstream uses: `:245` and `:250` both cite
the proposition only for the impossibility of constituting every prior from other latents. But it is
not enough for the first: a latent minimal among latents may still have observed parents, in which
case its factor is the conditional `p(latent | observed parents)`, not an unconditional marginal, and
"whose marginal law is therefore part of the declared parameters" fails.

So the load-bearing conclusion is true and cheaply provable; the intermediate step as written is not
established by the given proof and is false in general for the manuscript's own model class. Fix:
run the topological argument on the latent subgraph, replace "no parents" with "no latent parents,"
and replace "whose marginal law" with the conditional law given its non-latent parents — or state
the hypothesis that latents have no observed parents, which would need justifying against the
`P_θ(do, dY | X)` setup.

**Recorded as adjudicated-not-a-defect:** the selective-citation charge against `12_philosophy.tex`.
`thm:obs-agent-interaction-equivalence` lives in `05b`, and the chapter declines the strong
participatory reading in four separate places. Do not re-raise.

## V2 — appendix condition-number table

**Original (critical):** "The appendix publishes 16 measured quantities with no machine-readable
backing." Eight-row table at `appendix_numerical_provenance.tex:43-58`; the seven distinctive
mantissas grep to nothing in `run_checks.py`, `claims.json`, `current-results.json`.

**Verdict: PARTIALLY CONFIRMED. Critical downgraded to medium.**

Three corrections, each established by execution rather than argument.

The values are not unbacked. All sixteen reproduce bit-exactly from the frozen seed
`FACTORIZATION_PROTOCOL_SEED = 20260803` (`run_checks.py:91`), regenerated through the runner's own
`_default_factorization_schedule` and `_regenerate_factorization_case`; the runner raises if the
schedule differs from the frozen one (`:4297-4302`). The seven distinctive mantissas are also
present verbatim at `VERIFICATION.md:236-247`, which is SHA-256 governed — it is listed under
`required_paths` in `manifest-policy.json` and bound at
`/inventory_manifest/protocol_files/VERIFICATION.md` in `current-results.json`. The original grep
omitted `VERIFICATION.md`, which is the fourth artifact in the appendix's own package table at
`:17-18`. A recomputed value from a digest-bound generator is stronger evidence than the frozen
literal the finding proposed as the fix, not weaker.

The count is inflated roughly twofold. Eight of the sixteen are minima, and every one sits at or
within two ulps of the mathematical floor: kappa_2(A) = sigma_max/sigma_min >= 1 is a theorem, not
a measurement. Six rows publish exactly 1. Two more entries are a repeat, the global maximum being
identical to the general maximum. Seven distinct informative numbers.

The stale-artifact half of the indictment restates the manuscript's own fence.
`appendix_numerical_provenance.tex:147-150` already says the checked-in `current-results.json` is
the older 29-check artifact, that it is not evidence for the 30-check package, and that a governed
regeneration remains required. This bears directly on V1 and is carried into that adjudication.

**What survives, and it is real:** fourteen of the sixteen values are ungated. The `expected` block
at `run_checks.py:4999-5013` carries no numeric achieved range, only the string
`"achieved_condition_coverage_near_1e14": "global only"`. The sole mechanical gate is a two percent
band on the global maximum at `:4954-4956`. A regeneration would therefore PASS with different
per-stratum extrema while the printed table silently went wrong — a drift-detection hole in exactly
the place the appendix's own rule at `:28-30` promises to avoid. Fix: put the per-stratum extrema
into `expected` so a run gates them, or replace the printed digits with a pointer.

Severity is medium rather than critical because the numbers recompute, sit in a governed file, the
staleness is disclosed, and a repo-wide mantissa grep finds no other manuscript file resting on any
value in the table. Nothing in `01`-`12` or `appendix_claim_ledger.tex` loads on it.

**New finding surfaced during the attack (N1, medium):** the published 17-digit maxima carry about
three significant digits of information. They are bit-stable across two binary64 SVD paths
(`numpy.linalg.cond` and `scipy.linalg.svdvals` agree exactly) but differ from the exact value at
the third significant digit — the general maximum is `1.015265553314175e14` in binary64 against
`1.00823462218377e14` at 60 decimal digits, the expected kappa*eps error of roughly two percent.
The appendix's definition at `:41-42` is honest that the quantity is `numpy.linalg.cond` of the
regenerated matrix, but roughly fourteen of the seventeen printed digits are properties of an SVD
run rather than of the matrix. Fix: print the digits that are significant, or state that the value
is the binary64 estimate and give its accuracy.

**Falsification conditions on the adjudication** (would restore critical): reproduction failing
under a different LAPACK/BLAS or numpy build, since only one environment was tested (Python 3.14.4,
numpy 2.4.4, scipy 1.17.1); any manuscript body claim loading on one of the seven maxima as
evidence rather than as coverage disclosure; or git history showing the generator changed after the
table was written, which would make the bit-exact reproduction coincidence rather than provenance.

**Process note.** The original V2 carried no `Falsifies` condition. Because no stated observation
would have retracted it, the two-minute recomputation that overturned its central conclusion was
never attempted. This is the argument for the contract's sixth field.
