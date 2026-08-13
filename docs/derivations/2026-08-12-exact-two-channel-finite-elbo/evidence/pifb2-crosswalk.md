# PIFB2 crosswalk and operator ledger

The live PIFB2 manuscript defines (q_i,p_i) as laws on the state statistical manifold and
(s_i,r_i) as laws on the model-parameter statistical manifold. It calls (s_i) the slow
generative-model section and (r_i) its hyperprior. The exact-ELBO construction uses a joint private
recognition law (\zeta_i(dk,dm)), with (q_i,s_i) as its marginals.

The certified object is the **joint-typed lagged unit-coefficient two-channel scalar**
(\mathcal F_{\mathrm{JT},h}^{\mathrm{lag},1}). This table is a source comparison, not an identity
that renames the certified scalar as the literal PIFB2 functional.

| PIFB2 sector | Relation to the joint-typed scalar |
|---|---|
| (D_{\rm KL}(q_a\Vert p_a)) | Exact private marginal term at unit coefficient |
| (D_{\rm KL}(s_a\Vert r_a)) | Exact private model term at unit coefficient |
| Joint-private expected observation log likelihood | Exact once under the joint private law (\zeta_a) |
| Literal PIFB2 observation display (`PIFB2.tex:669` / `:689`) | **Typing mismatch; not matched by this theorem.** `:689` writes (\mathbb E_{q_i(c)}[\log p(o(c)\mid k_i,m_i)]) with (m_i) unbound and not among the functional's declared arguments at `:684`; `:669` drops (m_i) entirely. Equality to the literal term is not proved and is not currently well-posed. For a general correlated (\zeta), disintegrate (\zeta(dk,dm)=q(dk)t_k(dm)); the joint-minus-predictive negative-log-likelihood difference is (\mathbb E_q[D_{\rm KL}(t_k\Vert s^{(o,k)})-D_{\rm KL}(t_k\Vert s)]), which is sign-indefinite. Under the additional state-model mean-field restriction (t_k=s), it reduces to (\mathbb E_q[D_{\rm KL}(s\Vert s^{(o,k)})]\ge0), so only on that restriction is the theorem's joint-private negative-log-likelihood an upper bound; the gap can be unbounded in model uncertainty. Closure requires an author-approved convention that binds (m_i) and chooses the joint-private or predictive-marginal reading. Registered since `2026-08-12-pifb2-continuum-roadmap.md:104` and `rm-03-action-class.md:364-366` |
| (I_{\zeta_a}(K_a;M_a)) | Mandatory exact correction; zero only under state-model mean field |
| Weighted transported belief KL | Exact for lagged sources and a separate label-copy block |
| Belief categorical row KL | Exact at unit temperature |
| Weighted transported model KL | Exact for lagged model sources and a separate label-copy block |
| Model categorical row KL | Exact at unit temperature |
| Same-step live sources | Not established by this theorem |
| (\tau) other than one | Requires a tempered normalized model and normalizers |
| (\lambda_h) or adaptive (\alpha) other than one | Requires replicas, powers, or a separate precision model |
| Cell-volume continuum weights | Deterministic-action scaling, not the unmodified finite ELBO |
| Base gradients and curvature | Absent from this finite probability theorem |

Live source locations inspected on 2026-08-13 and bound to Research Git revision (`1793a4d566826266f222f027d1be69761beede1a`) with `manuscripts/PIFB2.tex` SHA-256 (`f80e6dabd9e5485649066e227e80beff1dd2b1082cf786bcdae83db8cbd080ec4`):

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
