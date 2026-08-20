<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-368c9400e04e0700491b5a05ce03b074b8d146fa7243ce2327638237ab24a718","schema_version":"rigorous-theory-search/v1","target_digest":"368c9400e04e0700491b5a05ce03b074b8d146fa7243ce2327638237ab24a718"} -->
# Manuscript-dependency investigator memo

This memo records a source-level dependency trace performed after the probability and
interpretation lanes. It is an implementation map, not evidence for a theorem.

## Minimal dependency graph

The existing include order can remain. The logical dependency becomes

\[
\begin{aligned}
&\text{agent law sections and model presentations}\\
&\longrightarrow
\text{finite agent blocks, evaluated mechanisms, local recognition laws, record kernels}\\
&\longrightarrow
\mathbb P_{\theta,V}
\text{ by normalized composition},
\qquad
\mathbb Q_{V,o,X}
\text{ by selected coupling}\\
&\longrightarrow
\text{evidence, posterior, and exact ELBO}\\
&\longrightarrow
\text{local conditional VFEs, pullback geometry, relational histories, and coarse laws}\\
&\longrightarrow
\text{participatory interpretation}.
\end{aligned}
\]

Chapter 3 may still prove generic Radon-Nikodym, relative-entropy, and regular-conditional results
before Chapter 4 constructs the admitted population law. Those theorems are parameterized by an
admitted probability kernel and do not make the population completion primitive.

## Minimal edit boundary

`Theory/01_introduction.tex:35-65` needs the local mechanism and coupling layer before its first
global ELBO display. `Theory/02_geometry.tex:67-78` and `Theory/02_geometry.tex:400-425` need the
model-law/evaluator clarification and an earlier agent preview. `Theory/03_probability.tex:24-99`
needs local blocks, interfaces, record-kernel types, and the coupling class before the population
completion interface. Its generic measure results at lines 153-418 should remain structurally
intact, while the recognition-marginal and compatibility material at lines 419-471 becomes a
two-level bridge from sections to agent-block laws and from agent-block laws to population
couplings.

`Theory/04_generative.tex:21-115` already supplies the ordered construction and needs a local-first
title, canonical full-law notation, bundled local mechanisms, and an abstract normalized
record-extension proposition. Its moving-target prohibition and undirected potential boundary at
lines 117-268 remain unchanged in content.

`Theory/05_elbo.tex:10-37` should define its correlated population recognition kernel as a
selected member of the earlier coupling class. The measure-level identity, equality criterion,
total-correlation correction, and E/M-coordinate results remain. `Theory/05b_local_collective_elbo.tex`
keeps the detailed record-kernel theorem, conditional/local objectives, and once-only factor
accounting. Moving its established label would break durable derivation-document consumers.

`Theory/12_philosophy.tex:19-72` and `Theory/12_philosophy.tex:251-315` receive the bounded
agent-relative interpretation. `Theory/SPEC.md` and `Theory/appendix_notation.tex` make the new
dependency and canonical symbols normative. `Theory/main.tex` needs no include-order change.
Later full-law tiers in the network-RG and hierarchical meta-agent chapters have distinct scopes
and should be inspected rather than mechanically renamed.

## Scope-sensitive notation migration

Foundational population uses of \(P_\theta\), \(Q_X\), their densities, evidence, and posterior
move to indexed blackboard-bold laws. Agent component kernels \(P_{\theta,i}^{m,k,o}\), model
samples \(m_i\), evaluated kernels \(K^X_{i,m_i}\), and normalized record kernels \(K_a\) retain
their meanings. The agent-block recognition law is new. Pairwise \(K_{ij}\) is only a local alias
for a uniquely owned pairwise record, never a generic potential.

Generic theorem-local \(P,Q\) remain allowed. Generic statistical families in later
information-geometric chapters retain their symbols when their scope is not the foundational
population law. Existing \(\mathbb P_I,\mathbb Q_I\) network-RG notation and the hierarchical
tower notation remain distinct. The final manuscript should not define duplicate aliases such as
\(\mathbb P_{\theta,V}:=P_\theta\).

The existing full-pointwise meta-agent design already reserves blackboard bold for full laws and
\(q_i^b,q_i^m\) for section values. The new \(\mathbb Q_{i,o,X}\) fills the previously unnamed
agent-block level without changing that policy.

## Stable labels

Chapter labels remain stable. Probability labels for regular conditionals, measurable RN
versions, common-reference densities, support/integrability hypotheses, recognition marginals,
and marginal nonuniqueness retain their roles. Existing interface labels for the structural
kernel signatures may change their displayed content but not their identifiers. The generative
gauge-covariance, exact normalization, moving-target, and evidence-invariance labels remain.

The exact-ELBO chapter and its extended-gap labels remain. In the local/collective chapter,
`prop:obs-interaction-normalization`, `hyp:local-interaction-kernels`,
`eq:obs-interaction-joint`, `eq:obs-global-ledger`, and
`eq:obs-singleton-incident-counting` remain in place. The generative chapter adds an abstract
construction seam instead of relocating those durable labels.

## Validation boundary

Residual foundational \(P_\theta,Q_X\) occurrences require inspection, not blind replacement,
because generic theorem scopes are valid. The implementation should run exact notation scans, a
clean LaTeX and bibliography cycle, undefined-reference and duplicate-label checks, the existing
theory verification tests, and the repository's authenticated manuscript-verification workflow.
The current full-pointwise notation scanner is bound to an older contract; it must be rebound
before its output can become release evidence.
