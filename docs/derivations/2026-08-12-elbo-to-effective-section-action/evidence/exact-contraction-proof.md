<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-4648de08bcb0913989cc11fb30c2da525d83bd93ccfbee6148f85ffff82db69c","schema_version":"rigorous-theory-search/v1","target_digest":"4648de08bcb0913989cc11fb30c2da525d83bd93ccfbee6148f85ffff82db69c"} -->
# Exact contraction and density-action theorem

Fix a finite lattice, finite agent count, standard-Borel microscopic space
\(Z_h\), and normalized microscopic posterior \(\Pi_{h,o}\). Let
\(C_h:Z_h\to X_h\) be a measurable coarse map that is fixed independently of
the recognition law. For a fine recognition law \(Q_h\), write
\(R_h=(C_h)_\#Q_h\) and \(P_{X,h}^o=(C_h)_\#\Pi_{h,o}\). Standard-Borel
disintegration and the chain rule for relative entropy give

\[
D_{\rm KL}(Q_h\Vert\Pi_{h,o})
=D_{\rm KL}(R_h\Vert P_{X,h}^o)
+\int D_{\rm KL}(Q_h(dz\mid x)\Vert\Pi_{h,o}(dz\mid x))\,R_h(dx).
\]

The second term is nonnegative and vanishes for the posterior-conditional
lift \(Q_h^\star(dz)=\int\Pi_{h,o}(dz\mid x)R_h(dx)\). Therefore

\[
\inf_{Q_h:(C_h)_\#Q_h=R_h}
\mathcal F_h(Q_h;o)
=-\log p_h(o)+D_{\rm KL}(R_h\Vert P_{X,h}^o).
\]

If \(P_{X,h}^o=Z_h^{-1}e^{-S_h}\nu_h\), then the exact contracted ELBO is

\[
\mathcal F_h^X(R_h;o)
=\mathbb E_{R_h}S_h-H_{\nu_h}(R_h)
+\log Z_h-\log p_h(o).
\]

Thus \(S_h=-\log[dP_{X,h}^o/d\nu_h]\), modulo an additive constant, is the
exact finite-lattice effective density action. The entropy, partition
normalizer, evidence, and discarded conditional KL are not optional. This
theorem does not imply that \(S_h\) is local, pairwise, or PIFB2-shaped.
