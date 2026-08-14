<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb","schema_version":"rigorous-theory-search/v1","target_digest":"b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb"} -->
# Counterexample register

## Selector and faithfulness controls

| ID | Claim or dropped hypothesis | Exact finite witness | Consequence |
| --- | --- | --- | --- |
| CE-SEL-REFINEMENT | one single-valued law section is natural under every admitted correlated split | fair source bit; \(R_{1/3}\) and \(R_{1/2}\); common fair/fair marginals; distinct atom multisets \(\{1/3,1/3,1/6,1/6\}\) and \(\{3/8,3/8,1/8,1/8\}\) | direct nonexistence; unequal absolute correlations survive every sample relabeling |
| CE-SEL-FAITHFUL | a marginal section is also a left inverse on all joints | \(Q_0=(1/4,1/4,1/4,1/4)\), \(Q_{1/2}=(3/8,1/8,1/8,3/8)\), and \(mQ_0=mQ_{1/2}\) | marginalization is noninjective, so \(Sm=\operatorname{id}\) is impossible |
| CE-PREPARATION-REMOVAL | local-product uniqueness without preparation arrows | restrict the morphism class to typed bijections; a fixed nonzero-correlation binary rule can remain relabeling-equivariant | preparation arrows are load-bearing for product uniqueness under the declared local class |
| CE-MARGINAL-COMPATIBILITY | every joint kernel acts on marginal-only data | XOR sends same-marginal sources \(Q_0\) and \(Q_1\) to different output laws | interaction-sensitive XOR has no descended \(\bar K\) and is not a marginal-only morphism |
| CE-SET-VALUED | a fiber-valued assignment resolves the law-valued contradiction | \(\mu\mapsto\{Q:mQ=\mu\}\) contains both correlated outputs | it is not the frozen single-valued signature and selects no VFE, Fisher family, or intervention object |

Full derivations: `evidence/natural-selector-no-go-proof.md`.

## Independently typed recovery controls

| ID | Factorization predicate | Exact witness | Consequence |
| --- | --- | --- | --- |
| CE-RECOVERY-VFE | full-joint VFE factors through \((mQ,mP,z)\) | \(P=Q_0\) uniform and \(Q_{1/2}\) correlated; all displayed marginals uniform; KL values zero and strictly positive | no function of marginal inputs can return every compatible full-joint VFE |
| CE-RECOVERY-FISHER | full-joint Fisher factors through the marginal-family map | six-bit \(Q^{(0)}_\theta\), \(Q^{(1/2)}_\theta\); identical singleton families; center tensors \(4I_6\) and \((65536/16383)I_6\) | a selected family, not one marginal law value, is required for full Fisher |
| CE-RECOVERY-INTERVENTION | typed interventions factor through observational marginals | August 13 direct, latent, and null-extended BSC presentations; same retained law; incompatible binary \(E\)- and \(N\)-intervention inventories | the observational forgetful fiber contains nonisomorphic enriched objects |
| CE-FISHER-BOUNDARY | positivity can be omitted from a Fisher-family claim | a categorical family with a zero atom and a tangent entering that atom | the score/Fisher expression can be singular; the proved witness remains in the positive interior |
| CE-FAMILY-POINT | equality at one parameter determines Fisher | constant fair Bernoulli versus \(\operatorname{Ber}(1/2+t)\) at \(t=0\) | one law value does not determine family derivatives or Fisher |

Full derivations and exact August 13/14 source dependencies: `evidence/recovery-factorization-no-go-proof.md`.

## Reference-relative selection controls

| ID | Load-bearing hypothesis | Exact witness | Consequence |
| --- | --- | --- | --- |
| CE-IPROJ-SUPPORT | \(m\in\operatorname{conv}T(\operatorname{supp}p)\) can be omitted | bit, \(p=\delta_0\), \(T(x)=x\), target \(m=1\) | the only feasible target law has infinite KL; no finite minimizer exists |
| CE-IPROJ-MINIMAL | the exponential multiplier is unique without statistic minimalization | bit statistic \(T(x)=(x,2x)\) | all multipliers with fixed \(\alpha_1+2\alpha_2\) give the same law |
| CE-IPROJ-BOUNDARY | one fixed-support exponential chart is smooth across all faces | fair bit reference, \(T(x)=x\), \(q_m=(1-m,m)\), \(\lambda=\log[m/(1-m)]\) | the multiplier diverges and support changes at \(m=0,1\), despite a mass-vector limit |
| CE-IPROJ-TRANSPORT | equivariance holds while the reference is held fixed | \(T(a)=T(b)=0,T(c)=1\), target \(1/2\), nonsymmetric \(p(a)\ne p(b)\), swap \(a,b\) | the optimizer splits the zero-statistic mass in the reference ratio and does not commute unless \(p\) is transported |
| CE-COMPLETION-AC | \(r\ll f_\#p\) can be omitted | bit, identity \(f\), \(p=\delta_0\), \(r=\delta_1\) | no finite-KL lift; unsupported \(0/0\) fiber |
| CE-COMPOSITION-REFERENCE | arbitrary stage references preserve strict nested composition | \(p=(1/2,1/4,1/8,1/8)\), two two-point \(f\)-fibers, collapsed \(g\), arbitrary intermediate reference \((1/2,1/2)\) | staged lift \((1/3,1/6,1/4,1/4)\) differs from direct lift \(p\) |
| CE-STOCHASTIC-RIGHT-INVERSE | deterministic completion extends to every stochastic channel | channel outputs a fair bit independently of input | its image contains only the fair law, so no right inverse exists for all targets |
| CE-ENVELOPE-FEASIBLE | the envelope differential ignores a moving feasible set | fixed uniform posterior and feasible singleton \(q_\theta=(1-\theta,\theta)\) | objective has zero explicit parameter derivative but optimized value generally has nonzero derivative |
| CE-ENVELOPE-UNIQUE | uniqueness and a fixed optimizer stratum can be omitted | recognition set \(\{\delta_0,\delta_1\}\) under a Bernoulli posterior crossing one half | two minimizers at the crossing and a nondifferentiable optimum |
| CE-VFE-EVIDENCE | retained posterior descent is defined on a zero-evidence slice | \(z=0\) | \(-\log z=+\infty\) and the posterior slice is undefined |

Full derivations: `evidence/reference-relative-selection-proof.md`.

## Scope

These controls refute only the matching frozen statements or demonstrate the necessity of named hypotheses. None is evidence against reference-relative selection under its proved finite support conditions, deterministic completion under absolute continuity, or retained descent under the complete August 13 equivalence.
