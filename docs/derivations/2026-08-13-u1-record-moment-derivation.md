# U(1) two-path record-moment derivation and presentation control

Consider the normalized equal-weight record mixture

\[
p_\Theta(do)=\frac12\,\mathcal N(do;R_{a_1}\mu,C_1)
+\frac12\,\mathcal N(do;R_{a_2}\mu,C_2),
\qquad a_1-a_2=\Theta,
\]

where each covariance is the rotated source covariance plus isotropic observation noise. Its
marginal record mean is

\[
m_\Theta=\mathbb E_{p_\Theta}[O]
=\frac12(R_{a_1}+R_{a_2})\mu
=\cos(\Theta/2)R_{a_1-\Theta/2}\mu .
\]

The squared norm

\[
S(\Theta):=\|m_\Theta\|^2
=\|\mu\|^2\frac{1+\cos\Theta}{2}
\]

is determined by the marginalized record law and is invariant under a common endpoint rotation.
For the declared \(\|\mu\|=1\), \(S(0)=1\) and \(S(\pi/2)=1/2\). Therefore the two selected record
laws are not gauge-equivalent. This exact moment argument, not a minimum over a sampled gauge grid,
is the load-bearing separation certificate.

The same calculation gives the exact equivalences used as controls:

- Replacing \(\Theta\) by \(\Theta+2\pi k\) adds \(k\varphi_0\) to both path angles, so the common
  gauge \(g=-k\varphi_0\) aligns the two component lists.
- The equal-weight laws at \(\Theta\) and \(2\pi-\Theta\) agree after the common gauge
  \(g=\pi/2+\Theta/2\) and interchange of the two path labels. The design cannot orient the pair.
- For \(A=d\lambda_\Theta\), with \(\lambda_\Theta(\varphi)=\Theta\sin\varphi/(2\pi)\), both routes
  have the same endpoint angle
  \(\alpha=\lambda_\Theta(\varphi_0)-\lambda_\Theta(0)\). The common gauge \(g=-\alpha\) maps the
  entire record law exactly to its \(\Theta=0\) representative. The raw law rotates with
  \(\Theta\); the invariant statement is membership in one gauge orbit.

Finally, define a zero-connection model whose two normalized label-conditional kernels carry the
ordinary group twists \((a_1,a_2)\). Its two Gaussian components are identical, term by term, to the
curve-transport components above. Consequently the record law is exactly the same. The witness
therefore establishes monodromy sensitivity inside the constrained curve-transport model, but does
not identify a connection origin among broader generative presentations. A proposed multi-point
cocycle discriminator remains open; neither necessity nor sufficiency has been proved.

The executable implementation and exact controls are in
`docs/verification/u1_two_path_holonomy_witness.py`; focused regression tests are in
`tests/test_u1_two_path_holonomy_witness.py`.
