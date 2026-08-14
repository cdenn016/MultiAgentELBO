<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2","schema_version":"rigorous-theory-search/v1","target_digest":"ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2"} -->
# Fixed-outside VFE and declared hyperedge record proof

## 1. Exact fixed-outside local/global difference

Let the finite state split as \(\Omega=\Omega_A\times\Omega_B\), where
\(A\) is one declared two-coordinate agent block and \(B\) is the four-bit
outside configuration. Let \(T,Q,Q'\) be strictly positive normalized laws
and suppose

\[
Q_B=Q'_B=m.
\]

Write \(q_b=Q_{A\mid B=b}\), \(q'_b=Q'_{A\mid B=b}\), and
\(t_b=T_{A\mid B=b}\). With
\(\mathcal F_T(Q)=D_{\rm KL}(Q\|T)\), finite KL disintegration gives

\[
\mathcal F_T(Q)
=D_{\rm KL}(m\|T_B)+\sum_bm(b)D_{\rm KL}(q_b\|t_b).
\]

Subtracting the corresponding expression for \(Q'\) proves

\[
\mathcal F_T(Q)-\mathcal F_T(Q')
=\sum_bm(b)\left[
D_{\rm KL}(q_b\|t_b)-D_{\rm KL}(q'_b\|t_b)
\right].\tag{1}
\]

If a fixed-record VFE includes a common evidence constant, that constant also
cancels. Equation (1) does not say the full local functional equals the global
functional; it says their differences agree after the common outside term is
removed.

For a normalized conditional tangent \(h_b\), with
\(\sum_ah_b(a)=0\) for every \(b\), let
\(q_b^\epsilon=q_b+\epsilon h_b\) on a positivity-preserving interval.
Termwise finite differentiation gives

\[
\left.\frac d{d\epsilon}\right|_0\mathcal F_T(mq^\epsilon)
=\sum_bm(b)\sum_ah_b(a)\log\frac{q_b(a)}{t_b(a)}.\tag{2}
\]

The \(+1\) derivative of \(u\log u\) cancels by tangent normalization.
The executable retains two distinct controls. The first takes
\(Q=Q_{\theta,1/4}\), \(Q'=Q_{\theta,1/2}\), and
\(T=Q_{\theta,-1/3}\). Their four-bit outside marginals agree exactly by the
proper-marginal theorem. Its differential is the directional derivative at
the base law along \(dQ=Q_{\theta,1/2}-Q_{\theta,1/4}\). It is labeled an
outside-marginal-preserving `kappa_lift` direction, not a single agent's
two-\(\theta\) coordinate update, and it is not the derivative per unit
\(\kappa\) unless divided by \(1/2-1/4\).

The second control is parameterized by agent-pair index. For each of the three
declared pairs \(A=\{i,j\}\) in turn, it fixes \(\kappa=1/2\), varies exactly
that pair's two \(\theta\) coordinates, and holds the complementary four
coordinates fixed in the base, alternate, and target laws. It checks exact
equality of the outside theta tuple, outside marginal, and zero outside
tangent. Its difference uses two distinct settings of the selected agent
block. Its differential uses the analytic tangent

\[
h(x)=v_i\partial_{\theta_i}Q_{\theta,\kappa}(x)
+v_j\partial_{\theta_j}Q_{\theta,\kappa}(x)
\]

at the base law. Therefore the three `agent_theta_block` controls directly
corroborate both (1) and (2) for every declared one-agent two-coordinate block.

## 2. Coherent finite covariance

For any finite bijection \(g:\Omega\to\Omega\),

\[
D_{\rm KL}(g_*Q\|g_*T)=D_{\rm KL}(Q\|T)
\]

by reindexing the finite sum. Thus the fixed-target VFE is covariant under a
declared paired complement or admitted coordinate relabeling only when the
target is pushed forward coherently with recognition. Pushing \(Q\) while
holding a noninvariant coordinate representative \(T\) fixed need not
preserve VFE. No broader gauge-covariance claim is implied.

## 3. Declared three-agent hyperedge record

At \(\theta_i=1/2\), set \(c=\kappa/64\) and use the uniform prior
\(\Pi(x)=1/64\). Declare one binary record kernel

\[
K(1\mid x)=\frac12(1+c\chi(x)),\qquad
K(0\mid x)=\frac12(1-c\chi(x)).\tag{3}
\]

Because \(|c|<1\), both values are strictly positive and sum to one.
Parity balance gives

\[
p(Y=1)=\sum_x\Pi(x)K(1\mid x)=\frac12.
\]

Bayes' rule then yields

\[
p(x\mid Y=1)
=\frac{\Pi(x)K(1\mid x)}{1/2}
=\frac{1+c\chi(x)}{64}
=Q_{\theta,\kappa}(x).\tag{4}
\]

For the correlated lift, recognition equals the posterior, so

\[
\mathcal F(Q_{\theta,\kappa};Y=1)=-\log p(Y=1)=\log2.\tag{5}
\]

For the product lift \(U=\Pi\),

\[
\mathcal F(U;Y=1)
=\log2+D_{\rm KL}\!\left(U\middle\|Q_{\theta,\kappa}\right)
=\log2-\frac12\log(1-c^2).\tag{6}
\]

The exact product-lift excess is therefore
\(-\tfrac12\log(1-c^2)>0\) for \(\kappa\ne0\).

Equation (3) is a declared and engineered three-agent hyperedge kernel. It is
not derived from the six singleton sections, pairwise locality, or an agency
principle. It supplies one observation model that selects the parity lift;
other kernels can select a different lift or no interaction at all.

## 4. Pairwise-product factorization is additional structure

Suppose two binary record marginals are declared by

\[
\Pr(Y_1=1\mid x)=\frac{1+a(x)}2,\qquad
\Pr(Y_2=1\mid x)=\frac{1+b(x)}2.
\]

The conditional-independence/product choice introduces an \(a(x)b(x)\) term
in the joint record kernel. That term can become a six-bit interaction when
the supports of \(a\) and \(b\) together cover all six coordinates. The
product choice is not implied by the two marginals.

Indeed, whenever \(|a(x)|,|b(x)|\le\eta<1/2\), define instead

\[
\begin{aligned}
q_{11}(x)&=\tfrac14(1+a+b),&
q_{10}(x)&=\tfrac14(1+a-b),\\
q_{01}(x)&=\tfrac14(1-a+b),&
q_{00}(x)&=\tfrac14(1-a-b).
\end{aligned}\tag{7}
\]

Every atom is at least \((1-2\eta)/4>0\), the four atoms sum to one, and

\[
q_{11}+q_{10}=\frac{1+a}2,\qquad
q_{11}+q_{01}=\frac{1+b}2.
\]

Thus (7) has exactly the same two marginal kernels as the factorized joint,
but its \(ab\) coefficient is zero. This same-marginal cancelling control
proves that pairwise-product observation factorization consumes an additional
conditional-independence assumption and that alternative joint kernels can
erase its six-bit term.
