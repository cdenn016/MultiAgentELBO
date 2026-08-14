# Exact derivations for the 2026-08-13 Claude Opus audit

Audit target: `f9ce06a5782dd5fd0392761cdd1872a983429326`.

These calculations are deliberately narrower than the surrounding research program. They establish
counterexamples or missing hypotheses for the claims named below; they do not establish a complete
agent-only ontology, a continuum limit, or a literal PIFB2 derivation.

## D1. Rank two can coexist with positive KL edge weights and a proper residual prior

Let

\[
D=I_4,\qquad T=I_2,\qquad
\Lambda=\begin{pmatrix}
1&1/10\\
1&1/5\\
1&3/10\\
1&2/5
\end{pmatrix},\qquad
\Sigma=D+\Lambda T\Lambda^{\mathsf T}.
\]

Woodbury gives

\[
P=\Sigma^{-1}=I_4-\Lambda(I_2+\Lambda^{\mathsf T}\Lambda)^{-1}\Lambda^{\mathsf T}.
\]

Direct exact arithmetic yields

\[
P=\begin{pmatrix}
87/110&-1/5&-21/110&-2/11\\
-1/5&4/5&-1/5&-1/5\\
-21/110&-1/5&87/110&-12/55\\
-2/11&-1/5&-12/55&42/55
\end{pmatrix}.
\]

For the unique scalar graph-Laplacian split, set \(\beta_{ab}=-P_{ab}\) for \(a\ne b\),
\(L(\beta)_{aa}=\sum_{b\ne a}\beta_{ab}\), and
\(\pi_a=P_{aa}-L(\beta)_{aa}\). Then

\[
\{\beta_{ab}:a<b\}
=\left\{\frac15,\frac{21}{110},\frac2{11},\frac15,\frac15,\frac{12}{55}\right\}>0,
\]

and

\[
\pi=\left(\frac{12}{55},\frac15,\frac2{11},\frac9{55}\right)>0.
\]

Moreover, \(P=L(\beta)+\operatorname{diag}\pi\) exactly and
\(\operatorname{rank}(I_4-P)=2\). Thus the universal claim that every
\(R\ge2\) shared-latent correction must lose positive KL weights is false. This does not prove that
an arbitrary directed row-simplex PIFB2 coupling has such a representation.

## D2. A free positive edge coefficient removes the claimed cocycle obstruction

Take three agents with \(K=d=2\), \(S_a=T=I_2\), and loading matrices
\(\Lambda_a=R_a\in SO(2)\). The stacked loading satisfies

\[
M=\left(T^{-1}+\sum_{a=1}^3\Lambda_a^{\mathsf T}S_a^{-1}\Lambda_a\right)^{-1}
=\frac14I_2.
\]

The effective precision has off-diagonal blocks

\[
P_{ab}=-S_a^{-1}\Lambda_aM\Lambda_b^{\mathsf T}S_b^{-1}
=-\frac14R_aR_b^{\mathsf T}.
\]

PIFB2's quadratic coefficient is a product \(-\beta_{ab}W_{ab}\Omega_{ab}\), not the transport
alone. Choose

\[
\beta_{ab}=\frac14,\qquad W_{ab}=I_2,\qquad
\Omega_{ab}=R_aR_b^{\mathsf T}.
\]

Then every precision cross-block is reproduced exactly, \(\Omega_{aa}=I_2\), and

\[
\Omega_{ab}\Omega_{bc}
=R_aR_b^{\mathsf T}R_bR_c^{\mathsf T}
=R_aR_c^{\mathsf T}
=\Omega_{ac}.
\]

The residual diagonal prior is \(I_2/4\succ0\). The sign contradiction in the audited proof arises
because it identifies the complete weighted coefficient with \(\Omega_{ab}\), effectively fixing
\(\beta_{ab}=1\). The counterexample refutes the universal cocycle no-go while leaving the attention
entropy and full recognition-law questions open.

## D3. The literal support mask removes the prior floor at departure

The PIFB2 self term has the form

\[
\chi_i\,\alpha_i D_{\mathrm{KL}}(q_i\Vert p_i).
\]

For a Gaussian mean perturbation, its local Hessian contribution is therefore

\[
H_i^{\mathrm{prior}}=\chi_i\alpha_i\Lambda_{p,i}.
\]

At an actual support departure \(\chi_i\to0\), both the pair weights
\(\chi_{ij}=\chi_i\chi_j\) and the local prior Hessian vanish for finite \(\alpha_i\). In the fixed
ambient coordinate space used by the witness, a departing agent with no other edges therefore adds a
zero \(K\times K\) row-and-column block and hence at least \(K\) exact zero modes. The witness instead
adds \(\alpha_i\Lambda_{p,i}\) without \(\chi_i\), so its positive spectral floor is a result for
edge dropout of a still-present anchored agent, not for the declared support boundary.

## D4. The directed forward-KL mean Hessian uses the transported second slot

For Gaussian laws

\[
q_i=\mathcal N(\mu_i,\Sigma_i),\qquad
\Omega_{ij\#}q_j=\mathcal N(\Omega_{ij}\mu_j,
\Omega_{ij}\Sigma_j\Omega_{ij}^{\mathsf T}),
\]

the mean-dependent part of the declared forward divergence is

\[
D_{\mathrm{KL}}(q_i\Vert\Omega_{ij\#}q_j)
=\frac12r_{ij}^{\mathsf T}
(\Omega_{ij}\Sigma_j\Omega_{ij}^{\mathsf T})^{-1}r_{ij}
+\text{terms independent of }r_{ij},
\]

where \(r_{ij}=\mu_i-\Omega_{ij}\mu_j\). Thus

\[
W_{i\leftarrow j}^{\mathrm{KL}}
=(\Omega_{ij}\Sigma_j\Omega_{ij}^{\mathsf T})^{-1}.
\]

The audited witness instead uses \(\Sigma_i^{-1}\). Its simultaneous-congruence theorem is valid for
that independently declared first-slot pencil, but it is not the Hessian of the stated directed KL
unless the additional edgewise equality
\(\Sigma_i=\Omega_{ij}\Sigma_j\Omega_{ij}^{\mathsf T}\) is imposed. The repository's Tier-0 document
explicitly says this shared-covariance hypothesis is not granted.

## D5. The four-regime table changes the operator outside the orthogonal group

The declared reverse link is \(\Omega_{ji}=\Omega_{ij}^{-1}\). The audited helper stores that inverse
but assembles the reverse block with \(\Omega_{ij}^{\mathsf T}\). These coincide only for orthogonal
links. Therefore the table's nonorthogonal cells are not evaluations of the declared inverse-link
operator. Independently sampled positive directed edge coefficients are also not a row-simplex law
until every receiver row is normalized. This invalidates the table's numerical attribution of
failure modes, although the active symmetric energy form and the algebraic reason for retiring the
old operator remain intact.

## D6. The Gibbs-Haar construction is exact only for a separately declared link-latent model

For compact \(G\), normalized Haar measure \(\mu_H\), and a bounded Wilson action \(S\), the law

\[
p_\beta(d\Theta)=Z_\beta^{-1}e^{-\beta S(\Theta)}\,\mu_H(d\Theta)
\]

is proper. For any recognition law \(q(\Theta)\ll\mu_H\), its variational free energy is

\[
\mathcal F[q]=\beta\,\mathbb E_q S+\mathbb E_q\log\frac{dq}{d\mu_H}
=-\log Z_\beta+D_{\mathrm{KL}}(q\Vert p_\beta).
\]

This establishes an exact realization for a newly declared random-link model. It does not insert the
same term into an existing model in which \(\Theta\) is fixed or point-estimated, and minimizing over
\(q\) returns the posterior rather than forcing a point link to zero curvature. The worklog display
omits \(\beta\), although its table uses \(\beta=2\).

## D7. Curvature, flatness, and retained modes are not equivalent

The exact connection-Laplacian result is

\[
\ker L\cong\operatorname{Fix}(\operatorname{Hol}).
\]

Two counterexamples separate the concepts.

1. Let a triangular \(SO(3)\) connection have holonomy \(R_z(0.6)\ne I\). The vector \(e_z\) is
   fixed, so the corresponding parallel section lies in \(\ker L\) even though the holonomy is
   nonidentity.
2. On a flat torus take commuting monodromies
   \(H_x=\operatorname{diag}(1,-1,-1)\) and
   \(H_y=\operatorname{diag}(-1,-1,1)\). Local plaquette curvature vanishes, but
   \(\operatorname{Fix}(H_x)\cap\operatorname{Fix}(H_y)=\{0\}\), so no nonzero retained mode exists.

Consequently \(\lambda_0=0\iff\) flat \(\iff\) meta-agent is false without additional topology and
representation hypotheses. A one-parameter numerical fit may remain valid on its sampled family.

## D8. A toroidal interaction graph does not determine base-bundle topology

The interaction complex and contextual base are independent declared objects in the governing
theory. A contractible base with a toroidal interaction graph can carry graph monodromy while the base
bundle is trivial. Conversely, a nontrivial bundle over \(S^2\) can be paired with a tree interaction
graph. Graph cycles can probe base topology only after declaring vertex anchors, edge paths or a
cellular map into the base, and equality between graph links and the corresponding connection
parallel transports.

## D9. Nontransitive statistical fibers can still have nontrivial gauge actions

For a Gamma law in shape-rate coordinates, scaling the sample by \(c>0\) gives

\[
X\sim\Gamma(a,b)\quad\Longrightarrow\quad cX\sim\Gamma(a,b/c).
\]

This is a continuous nontrivial pushforward action that preserves shape and is therefore not
transitive on the full two-dimensional family. With Fisher matrix

\[
g(a,b)=\begin{pmatrix}
\psi_1(a)&-1/b\\
-1/b&a/b^2
\end{pmatrix}
\]

and parameter map \(\phi_c(a,b)=(a,b/c)\), whose Jacobian is
\(J=\operatorname{diag}(1,1/c)\), direct substitution gives

\[
J^{\mathsf T}g(a,b/c)J=g(a,b).
\]

Thus nonconstant curvature rules out transitivity, not every nontrivial gauge action. Homogeneity is a
sufficient condition for one-orbit gauge reach, not a necessary condition for associated-bundle
gauge structure.

## D10. Homogeneous does not imply symmetric

For the affine Gaussian group, take

\[
\mathfrak g=\mathfrak{gl}(K)\ltimes\mathbb R^K,\qquad
\mathfrak h=\mathfrak{so}(K),\qquad
\mathfrak m=\operatorname{sym}(K)\oplus\mathbb R^K.
\]

For \(X=(S,0)\in\mathfrak m\) and \(Y=(0,v)\in\mathfrak m\),

\[
[X,Y]=(0,Sv)\in\mathfrak m
\]

generically, not in \(\mathfrak h\). Hence the symmetric-pair condition
\([\mathfrak m,\mathfrak m]\subseteq\mathfrak h\) fails for the full location-covariance family.
The covariance cone \(SPD(K)=GL(K)/O(K)\) is symmetric; a general homogeneous statistical manifold
need only be a homogeneous space \(G/H\).

## D11. Latent dimension alone does not imply induced-transport invertibility

The block

\[
\Lambda_aM\Lambda_b^{\mathsf T}S_b^{-1}
\]

has rank at most
\(\min\{\operatorname{rank}\Lambda_a,\operatorname{rank}\Lambda_b,\operatorname{rank}M,K\}\).
Therefore \(d\ge K\) is necessary but not sufficient. With \(d=K=2\),
\(M=S_b=I_2\), and

\[
\Lambda_a=\Lambda_b=\begin{pmatrix}1&0\\0&0\end{pmatrix},
\]

the induced block has rank one and determinant zero. Likewise, the Woodbury correction rank equals
the latent dimension only when the stacked loading has the corresponding full column rank and the
latent covariance is nondegenerate.

## D12. The scalar split is not literally the complete PIFB2 action

The rank-one construction exactly yields a symmetric, unnormalized scalar Laplacian quadratic and a
residual diagonal. Literal PIFB2 additionally specifies directed row-normalized attention,
source-label entropy and prior terms, transported belief/model laws, and proper probabilistic typing.
The residual diagonal in the witness can be negative. The correct result name is therefore an exact
flat scalar mean-alignment skeleton, not "exactly PIFB2." This renaming preserves the useful algebra.

## D13. Dropped candidate: compact links under compact vertex gauges are closed

The governing graph-link definition uses one group \(G\) for both
\(\Theta_e\in G\) and vertex reframings \(a_i\in G\), with
\(\Theta'_e=a_i^{-1}\Theta_ea_j\). Once the declaration sets this same \(G\) to a compact subgroup,
group closure gives \(\Theta'_e\in G\). The audit candidate that retained full-\(GL(K)\) vertex gauges
while restricting only links read two different groups into a one-group definition and is therefore
dropped. The documents would still benefit from saying explicitly that the compact declaration
restricts vertex gauges as well as link values.
