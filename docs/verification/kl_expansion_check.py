"""Second/third-order KL expansion and lattice-stencil cancellation check.

Supports section 2 of docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md.

Establishes, for regular exponential families q_theta(x) = exp(theta*T(x) - A(theta))
with Fisher metric g^F = A''(theta) and Amari-Chentsov skewness tensor T_skew = A'''(theta):

    KL(q_{theta+h} || q_theta) = (1/2) g^F h^2 + (1/3) T_skew h^3 + O(h^4)
    KL(q_theta || q_{theta+h}) = (1/2) g^F h^2 + (1/6) T_skew h^3 + O(h^4)

and that the h^3 term, being odd in h, cancels on a symmetric nearest-neighbour
stencil in both argument orders. Hence with weight h^{d-2},

    sum_{<c,c'>} h^{d-2} KL(q(c) || q(c'))  ->  (1/2) int ||grad q||^2_{g^F} dc

with no surviving Amari-Chentsov correction and relative error O(h^2).

SCOPE: flat / trivial-transport case only. With a nontrivial connection the two
neighbours are compared through different transports Omega_{c,c+h} vs Omega_{c,c-h};
the transport contributes its own O(h) piece and the odd/even cancellation must be
re-established covariantly. That is not checked here.

Run:  python docs/verification/kl_expansion_check.py
Requires: sympy.
"""

import sympy as sp

th, h, t = sp.symbols('theta h t', real=True)


def kl_gauss(m1, s1, m0, s0):
    """Closed-form KL( N(m1, s1^2) || N(m0, s0^2) )."""
    return sp.log(s0 / s1) + (s1**2 + (m1 - m0)**2) / (2 * s0**2) - sp.Rational(1, 2)


def check_gaussian_scale_family():
    """Concrete family with a nonzero third-order term, and its stencil cancellation."""
    print("=" * 74)
    print("Gaussian scale family: sigma(t) = exp(t), mean fixed at 0")
    print("=" * 74)
    fwd = sp.expand(sp.series(kl_gauss(0, sp.exp(t), 0, 1), t, 0, 6).removeO())
    rev = sp.expand(sp.series(kl_gauss(0, sp.exp(-t), 0, 1), t, 0, 6).removeO())
    print(f"  KL(q(+t)||q(0)) = {fwd}")
    print(f"  KL(q(-t)||q(0)) = {rev}")
    print(f"    t^2 coefficients: {fwd.coeff(t,2)}, {rev.coeff(t,2)}"
          "   (Fisher for theta=log sigma is 2, so (1/2)g^F = 1)")
    print(f"    t^3 coefficients: {fwd.coeff(t,3)}, {rev.coeff(t,3)}   <- equal and opposite")
    pair = sp.expand(fwd + rev)
    print(f"  symmetric stencil sum = {pair}")
    print(f"    t^3 coefficient of the pair sum: {pair.coeff(t,3)}   <- cancels exactly")
    assert pair.coeff(t, 3) == 0
    print()


def check_exponential_family(name, A_expr):
    """Verify the (1/2, 1/3) and (1/2, 1/6) coefficients for a concrete log-partition A."""
    A = lambda z: A_expr.subs(th, z)
    Ap = lambda z: sp.diff(A_expr, th).subs(th, z)

    # KL(q_{th+h} || q_th) = h*A'(th+h) - A(th+h) + A(th)
    fwd = sp.expand(sp.series(h * Ap(th + h) - A(th + h) + A(th), h, 0, 5).removeO())
    # KL(q_th || q_{th+h}) = A(th+h) - A(th) - h*A'(th)
    bwd = sp.expand(sp.series(A(th + h) - A(th) - h * Ap(th), h, 0, 5).removeO())

    A2 = sp.diff(A_expr, th, 2)
    A3 = sp.diff(A_expr, th, 3)
    print(f"--- {name}:  A = {A_expr}")
    out = {}
    for lbl, key, s in (("KL(q_{th+h} || q_th)", 'fwd', fwd),
                        ("KL(q_th || q_{th+h})", 'bwd', bwd)):
        r2 = sp.simplify(s.coeff(h, 2) / A2)
        r3 = sp.simplify(s.coeff(h, 3) / A3)
        print(f"    {lbl}:  h^2 -> {r2} * g^F      h^3 -> {r3} * T_skew")
        out[key] = (r2, r3)
    assert out['fwd'] == (sp.Rational(1, 2), sp.Rational(1, 3)), out['fwd']
    assert out['bwd'] == (sp.Rational(1, 2), sp.Rational(1, 6)), out['bwd']
    # stencil cancellation: replace h -> -h and add
    for s in (fwd, bwd):
        pair = sp.expand(s + s.subs(h, -h))
        assert sp.simplify(pair.coeff(h, 3)) == 0
    print("    symmetric stencil sum: h^3 coefficient cancels in both orders. OK")


def main():
    check_gaussian_scale_family()
    print("=" * 74)
    print("Generic exponential families: coefficient verification")
    print("=" * 74)
    check_exponential_family("Poisson", sp.exp(th))
    check_exponential_family("Bernoulli", sp.log(1 + sp.exp(th)))
    check_exponential_family("Exponential (rate)", -sp.log(-th))
    print()
    print("All assertions passed.")
    print()
    print("    KL(q_{theta+h} || q_theta) = (1/2) g^F h^2 + (1/3) T_skew h^3 + O(h^4)")
    print("    KL(q_theta || q_{theta+h}) = (1/2) g^F h^2 + (1/6) T_skew h^3 + O(h^4)")
    print()
    print("  Same Fisher term at second order; argument order visible only at third,")
    print("  where the two differ by (1/6) T_skew h^3. The h^3 term is odd in h and")
    print("  cancels on a symmetric stencil, so the h^{d-2}-weighted lattice sum")
    print("  converges to the Fisher Dirichlet energy with relative error O(h^2).")


if __name__ == "__main__":
    main()
