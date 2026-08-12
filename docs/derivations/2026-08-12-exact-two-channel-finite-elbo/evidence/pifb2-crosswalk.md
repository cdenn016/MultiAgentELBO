# PIFB2 crosswalk and operator ledger

The live PIFB2 manuscript defines (q_i,p_i) as laws on the state statistical manifold and
(s_i,r_i) as laws on the model-parameter statistical manifold. It calls (s_i) the slow
generative-model section and (r_i) its hyperprior. The exact-ELBO crosswalk uses a joint private
recognition marginal (\zeta_i(dk,dm)), with (q_i,s_i) as its marginals.

| PIFB2 sector | Tied-replica status |
|---|---|
| (D_{\rm KL}(q_a\Vert p_a)) | Exact private marginal term at unit coefficient |
| (D_{\rm KL}(s_a\Vert r_a)) | Exact private model term at unit coefficient |
| Expected observation log likelihood | Exact once under the joint private law (\zeta_a) |
| (I_{\zeta_a}(K_a;M_a)) | Mandatory exact correction; zero only under state-model mean field |
| Weighted transported belief KL | Exact for lagged sources and a separate label-copy block |
| Belief categorical row KL | Exact at unit temperature |
| Weighted transported model KL | Exact for lagged model sources and a separate label-copy block |
| Model categorical row KL | Exact at unit temperature |
| Same-step live sources | Not established by this theorem |
| τ other than one | Requires a tempered normalized model and normalizers |
| λ_h or adaptive α other than one | Requires replicas, powers, or a separate precision model |
| Cell-volume continuum weights | Deterministic-action scaling, not the unmodified finite ELBO |
| Base gradients and curvature | Absent from this finite probability theorem |

Revision-bound live source locations inspected on 2026-08-12:

- `Research/manuscripts/PIFB2.tex:155-176`: state and model statistical manifolds.
- `Research/manuscripts/PIFB2.tex:663-713`: two-channel PIFB2 scalar.
- `Research/manuscripts/PIFB2.tex:929-954`: imposed fast-belief/slow-model hierarchy.
- `Research/manuscripts/magent_elbo_whitepaper/09_pifb2_crosswalk.tex:8-77`: joint private
  state-model recognition and the canonical two-channel crosswalk.
- `Research/manuscripts/magent_elbo_whitepaper/06_mean_field_theory.tex:393-470`: existing
  source-label lift, ordered-mask requirement for shared simultaneous variables, and self-slot
  entropy cost.

The present witness differs from the existing simultaneous shared-variable lift. It freezes source
laws in the previous history and gives every receiver independent relational copies. Consequently
reciprocal source graphs do not create a generative normalization cycle. The cost is interpretive:
the construction proves an exact adaptive representational lift, not same-time collective
emergence or literal identity of the replicas.
