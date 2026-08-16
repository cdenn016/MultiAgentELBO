<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Phase 0 notation standard

This standard is normative for the full pointwise parent program. It fixes symbols and their types; it proves no theorem. The primary tier consists of normalized laws and Markov kernels on declared standard-Borel spaces. Smooth statistical-manifold structure requires separate differentiability-in-quadratic-mean, domination, score-integrability, and Fisher-regularity hypotheses. Gaussian families are optional computational realizations only.

## Canonical registry

| Concept | Canonical symbol | Type and collision rule |
|---|---|---|
| Contextual base | $\mathcal C$ | Fixed contextual base; not time, RG depth, an intervention input, or an agent set. |
| Agent support | $\mathcal C_i$ | Domain on which agent $i$ supplies its local section pair. |
| Common overlap | $\mathcal U_A=\bigcap_{i\in A}\mathcal C_i$ | Shared patch for $A$; ordinary $R$ is not an overlap region. |
| Pointwise context | $r_*\in\mathcal U_A$ | One fixed base point for this program. |
| Principal bundle | $\mathscr P_G\to\mathcal C$ | Common principal $G$-bundle; bare $P$ is forbidden for this global object. |
| Scale principal bundle | $\mathscr P_\ell\to\mathcal C_\ell$ | Bundle at RG scale $\ell$; it is distinct from the root bundle $\mathscr P_G\to\mathcal C$. |
| Associated projection | $\varpi_x:\mathcal E_x\to\mathcal C$ | Bundle projection only; $\varpi_i$ is never receiver occupancy. |
| Belief-law section | $q_i^{b;o,X}$ | Normalized law-valued local section with admitted $o$ and fixed $X$ visible. Established $q_i^{o,X}$ remains valid typed source notation. |
| Model-law section | $q_i^{m;o,X}$ | Normalized law on $\mathsf M_i$ with admitted $o$ and fixed $X$ visible. Established $s_i^{o,X}$ remains valid typed source notation. |
| Model sample | $m_i\in\mathsf M_i$ | Coordinate or presentation, never a model law. |
| Model evaluation | $\operatorname{ev}_i(m_i)=K^X_{i,m_i}$ | Measurable normalized generative-kernel evaluation at fixed structural $X$. |
| Structural datum | $X$, $X_A=\chi_A(X)$ | Fixed conditioning data outside the random coarse channel. |
| Parent interface | $\xi_A\in\boldsymbol\Xi_A$ | Retained random boundary or interface coordinate, distinct from $X_A$. |
| Parent random state | $\mathsf Z_A=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A$ | Random retained state only. |
| Fine generative joint | $\mathbb P_I(Do,DY\mid X)$ | Fixed normalized law; it is assembled before recognition or posterior data. |
| Fine recognition law | $\mathbb Q_{I,o,X}$ | Normalized correlated law with every $o,X$ dependency retained. |
| Fine posterior | $\boldsymbol\Pi_{I,o,X}$ | Selected posterior version derived from $\mathbb P_I(\cdot\mid X)$. |
| Parent generative joint | $\mathbb P_A(Do,Dz\mid X)$ | Observation-preserving common-channel pushforward. Bare global $P_A$ is forbidden. |
| Parent recognition law | $\mathbb Q_{A,o,X}$ | Common-channel pushforward of $\mathbb Q_{I,o,X}$. Bare global $Q_A$ is forbidden. |
| Parent posterior | $\boldsymbol\Pi_{A,o,X}$ | Common-channel pushforward of the selected fine posterior. |
| Parent recognition marginals | $q_A^b,q_A^m$ | Derived projections of $\mathbb Q_{A,o,X}$ at locally fixed $(o,X)$; never substitutes for the correlated full law. |
| Parent prior marginals | $p_A^b,p_A^m$ | Derived projections of the typed parent generative conditional; not independently chosen priors. |
| Parent posterior marginals | $\boldsymbol\Pi_{A,o,X}^b,\boldsymbol\Pi_{A,o,X}^m$ | Derived projections of the selected parent posterior; not recognition marginals. |
| Parent evaluation | $\operatorname{ev}_A(m_A)=K^{X_A}_{A,m_A}$ | Measurable normalized kernel in $\operatorname{Kern}(\boldsymbol\Xi_A,\mathsf B_A\times\mathsf O_A\times\mathsf H_A)$. |
| Coarse channel | $C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A$ | One normalized recognition-independent Markov kernel. It is not an aggregation matrix or deterministic moving map. |
| Moving deterministic map | $c_t$ | Smooth special case used only after a dynamics is declared; it is not $C_A$. |
| Receiver occupancy | $\alpha_i^x$ | External positive normalized receiver mass for channel $x$; not a learned attention parameter or logit. |
| Conditional attention rows | $\beta_{ij},\gamma_{ij}$ | Belief- and model-channel conditional source rows; neither row determines receiver occupancy. |
| Joint edge event | $\eta_{ij}^q=\alpha_i^q\beta_{ij}$ and $\eta_{ij}^m=\alpha_i^m\gamma_{ij}$ | Normalized marked edge-event laws; exact attention RG pushes these laws, not rows alone. |
| Intervention chain | $R\to E\to O$ | Retained input or parameter, intervened target, and retained output or observation. |
| Action | $\mathscr S$ | Variational action; lowercase behavioral action requires a later declaration. |

## Collision and migration contract

One canonical token has one semantic type in a theorem. A type change requires another symbol. Bare $P,Q$ are allowed only as lemma-local dummy probability measures after a nearby type declaration. The principal object is always $\mathscr P_G$; full laws use $\mathbb P$, $\mathbb Q$, and $\boldsymbol\Pi$.

The sample $m_i\in\mathsf M_i$ is not law-valued. Only frozen pointwise-RG passages that explicitly typed an old $m_i$ as a law may document it as the local legacy alias of $q_i^m$. Likewise, historical root marginals $Q_q,Q_m$ are legacy aliases of $q_A^b,q_A^m$ at locally fixed $(o,X)$. They do not determine a parent joint. Established $q_i^{o,X},s_i^{o,X}$ retain their explicit dependencies and are not globally renamed.

The geometric $\varpi_i$ remains valid when it is explicitly the projection of agent $i$'s paired bundle. Receiver occupancy remains $\alpha_i^x$. The coarse symbol $C_A$ is a Markov kernel only; a deterministic moving map is $c_t$. Structural $X$ and $X_A=\chi_A(X)$ remain outside $C_A$. The comparison package retains the typed chain $R\to E\to O$.

Released derivation packages and audits are immutable evidence. Their old spellings are classified as `immutable_evidence`, not migrated. Active-source legacy spellings are accepted only when the registry supplies the same alias, type, and scope and the occurrence is semantically recognizable. Every other collision is `unclassified_collision` and makes the scanner fail.

## Scanner contract

`notation_scan.py` validates the registry before reading sources, classifies active and immutable occurrences, sorts every path/line/token record, and writes deterministic UTF-8 JSON with one terminal LF. It fails closed on an invalid registry, any unclassified active collision, occupancy written as $\varpi_i$, a new bare global $P_A$ or $Q_A$, a law-valued sample $m_i$, or a use of $C_A$ as both kernel and matrix/operator. Its self-test also verifies immutable-history acceptance and locally declared dummy $P,Q$ acceptance.
