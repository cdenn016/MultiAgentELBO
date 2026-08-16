"""Finite reconstruction of direct-derivation.md section 7 (2026-08-15 package).

Three checks, all on finite spaces so every measure is an explicit vector:

  C1  The section-7 identity  (T_A)_# (mu C_A) = [(T_I)_# mu] C_A'  holds for EVERY mu
      given only the channel intertwining (7.4). It does not use (7.2) or (7.3).

  C2  Isotropy specialization: with source/target identified, (7.2) reads
      (T_I)_# Pi_I = Pi_I, and the conclusion (7.5) reads (T_A)_# Pi_A = Pi_A.
      Verified on the parity model the investigator supplies.

  C3  The genuine-erasure datum: C_A blind to the coordinate T_I moves,
      T_A = id.  Parent law invariant while the fine law is NOT.  Check that
      (7.4) HOLDS (with T_A = id) and (7.2) FAILS, i.e. the datum is excluded
      from ASM-HOLONOMY-BLIND-DATA yet exhibits exactly what "blind" connotes.
      Also check that C1 still delivers the erasure conclusion for this datum,
      i.e. the erasure theorem is the T_A = id instance of section 7's own step.
"""

from itertools import product
import random

FINE = list(product([0, 1], repeat=2))          # Y_I = {0,1}^2
COARSE = [0, 1]                                 # Z_A = {0,1}


def push(T, mu):
    """(T)_# mu for a map T on a finite space; mu is a dict."""
    out = {}
    for y, p in mu.items():
        out[T(y)] = out.get(T(y), 0.0) + p
    return out


def apply_kernel(mu, C, codomain):
    """mu C  as a dict on codomain; C(y) is a dict on codomain."""
    out = {z: 0.0 for z in codomain}
    for y, p in mu.items():
        for z, q in C(y).items():
            out[z] += p * q
    return out


def close(a, b, tol=1e-12):
    keys = set(a) | set(b)
    return all(abs(a.get(k, 0.0) - b.get(k, 0.0)) < tol for k in keys)


def check_74(C, C_prime, T_I, T_A, domain, codomain):
    """(7.4):  C'(T_I Y, D) = C(Y, (T_A)^{-1} D)   for all Y and all D."""
    inv_TA = {}
    for z in codomain:
        inv_TA.setdefault(T_A(z), []).append(z)
    for y in domain:
        lhs = C_prime(T_I(y))
        rhs_raw = C(y)
        # C(y, T_A^{-1} D) as a measure in the D variable = (T_A)_# C(y, .)
        rhs = {}
        for z, p in rhs_raw.items():
            rhs[T_A(z)] = rhs.get(T_A(z), 0.0) + p
        if not close(lhs, rhs):
            return False
    return True


print("=" * 72)
print("MODEL 1 (investigator's parity model): C_A = parity, T_I flips y1, T_A flips z")
print("=" * 72)

C_parity = lambda y: {(y[0] ^ y[1]): 1.0}
T_I_1 = lambda y: (1 ^ y[0], y[1])
T_A_1 = lambda z: 1 ^ z

print("(7.4) holds with BOTH actions nontrivial:",
      check_74(C_parity, C_parity, T_I_1, T_A_1, FINE, COARSE))

# C1: the identity holds for EVERY mu, using only (7.4).
random.seed(0)
worst = 0.0
for trial in range(2000):
    w = [random.random() for _ in FINE]
    s = sum(w)
    mu = {y: wi / s for y, wi in zip(FINE, w)}
    lhs = push(T_A_1, apply_kernel(mu, C_parity, COARSE))
    rhs = apply_kernel(push(T_I_1, mu), C_parity, COARSE)
    worst = max(worst, max(abs(lhs.get(z, 0.) - rhs.get(z, 0.)) for z in COARSE))
print("C1  max |(T_A)_#(mu C_A) - [(T_I)_#mu] C_A'| over 2000 random mu :", worst)
print("    -> the section-7 step is an identity in mu; (7.2)/(7.3) are NOT used in it.")

# C2: isotropy specialization on the uniform (invariant) fine law.
Pi_I = {y: 0.25 for y in FINE}
print("C2  (7.2) at the isotropy arrow, (T_I)_#Pi_I == Pi_I :",
      close(push(T_I_1, Pi_I), Pi_I), "   <-- this IS fine-level invariance, assumed")
Pi_A = apply_kernel(Pi_I, C_parity, COARSE)
print("    conclusion (7.5), (T_A)_#Pi_A == Pi_A                :",
      close(push(T_A_1, Pi_A), Pi_A), "   <-- inherited in one substitution")

# Non-invariant fine law under the SAME model: parent is then NOT invariant.
Pi_bad = {(0, 0): 1.0}
Pi_bad_A = apply_kernel(Pi_bad, C_parity, COARSE)
print("    drop (7.2): mu = delta_(0,0),  (T_A)_#(mu C_A) == mu C_A ? ",
      close(push(T_A_1, Pi_bad_A), Pi_bad_A),
      "  <-- parent invariance FAILS without the fine hypothesis")

print()
print("=" * 72)
print("MODEL 2 (genuine erasure): C_A reads y1 only, T_I flips y2, T_A = id")
print("=" * 72)

C_proj = lambda y: {y[0]: 1.0}
T_I_2 = lambda y: (y[0], 1 ^ y[1])
T_A_2 = lambda z: z

print("(7.4) holds (it reduces to channel invariance C_A(T_I Y,D)=C_A(Y,D)) :",
      check_74(C_proj, C_proj, T_I_2, T_A_2, FINE, COARSE))

mu_ne = {(0, 0): 1.0}
print("fine law NOT invariant:  (T_I)_#mu == mu ?",
      close(push(T_I_2, mu_ne), mu_ne))
lhs = apply_kernel(push(T_I_2, mu_ne), C_proj, COARSE)
rhs = apply_kernel(mu_ne, C_proj, COARSE)
print("parent law IS blind:     [(T_I)_#mu] C_A == mu C_A ?", close(lhs, rhs))
print("  -> this is (*) with STRICT inequality upstream: exactly what 'blind' connotes.")

worst2 = 0.0
for trial in range(2000):
    w = [random.random() for _ in FINE]
    s = sum(w)
    mu = {y: wi / s for y, wi in zip(FINE, w)}
    a = apply_kernel(push(T_I_2, mu), C_proj, COARSE)
    b = apply_kernel(mu, C_proj, COARSE)
    worst2 = max(worst2, max(abs(a.get(z, 0.) - b.get(z, 0.)) for z in COARSE))
print("erasure holds for EVERY mu, max deviation over 2000 random mu :", worst2)
print("  -> the 'missing' erasure theorem is the T_A = id instance of C1,")
print("     i.e. of the very computation displayed at direct-derivation.md:443-445.")

print()
print("Isotropy admissibility of MODEL 2 under ASM-HOLONOMY-BLIND-DATA:")
print("  (7.2) requires (T_I)_#Pi_I = Pi'_I ; at an isotropy arrow with identified")
print("  spaces Pi'_I = Pi_I, so (7.2) demands fine invariance. For mu = delta_(0,0)")
print("  this FAILS:", close(push(T_I_2, mu_ne), mu_ne),
      " -> the datum is EXCLUDED from the certified branch.")
