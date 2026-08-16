"""Independent finite verification of the load-bearing steps of
docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md

Checks (exact rationals for measures, float for logs):
  (3.1)/(3.3) parent normalization and observation-marginal preservation
  (3.5)       Pi_{I,o,X} C_A is a regular conditional of Z given O under P_A
  (3.6)       Q_A << Pi_A
  (6.2)       joint-lift RN derivative equals the fine derivative r(Y)
  (6.4)       extended KL chain identity  KL(Q_I||Pi_I) = KL(Q_A||Pi_A) + Delta_A
  (6.10/6.11) reverse-kernel recovery identities
  NECESSITY   the "observation unchanged" hypothesis is load-bearing:
              if the channel also coarsens O, the pushforward of the fine
              posterior is NOT a version of the parent posterior.
"""
from fractions import Fraction as F
from math import log
import itertools

O = ['a', 'b']
Y = [0, 1, 2]
Z = ['u', 'v']          # non-injective coarse space (|Z| < |Y|)

# ---- fine generative joint P_I(o,y) ------------------------------------
P_I = {('a', 0): F(1, 8), ('a', 1): F(1, 4), ('a', 2): F(1, 8),
       ('b', 0): F(1, 8), ('b', 1): F(1, 8), ('b', 2): F(1, 4)}
assert sum(P_I.values()) == 1

nu = {o: sum(P_I[(o, y)] for y in Y) for o in O}
Pi_I = {o: {y: P_I[(o, y)] / nu[o] for y in Y} for o in O}   # selected version

# ---- Markov channel C_A : Y -> Z (non-injective, normalized) ----------
C = {0: {'u': F(3, 4), 'v': F(1, 4)},
     1: {'u': F(1, 2), 'v': F(1, 2)},
     2: {'u': F(1, 4), 'v': F(3, 4)}}
for y in Y:
    assert sum(C[y].values()) == 1

# ---- admitted observation and recognition law -------------------------
o_star = 'a'
Q_I = {0: F(1, 6), 1: F(1, 2), 2: F(1, 3)}       # << Pi_I[a] (full support)
assert sum(Q_I.values()) == 1

# ---- (3.1) parent joint ------------------------------------------------
P_A = {(o, z): sum(P_I[(o, y)] * C[y][z] for y in Y) for o in O for z in Z}
assert sum(P_A.values()) == 1, "parent normalization FAILED"
nu_A = {o: sum(P_A[(o, z)] for z in Z) for o in O}
assert nu_A == nu, "(3.3) observation marginal NOT preserved"
print("(3.1)/(3.3) parent normalized, observation marginal preserved: OK")

# ---- (3.5) Pi_A = Pi_I C_A is a version of the parent posterior --------
Pi_A_push = {o: {z: sum(Pi_I[o][y] * C[y][z] for y in Y) for z in Z} for o in O}
Pi_A_cond = {o: {z: P_A[(o, z)] / nu_A[o] for z in Z} for o in O}
assert Pi_A_push == Pi_A_cond, "(3.5) pushforward is NOT the parent posterior"
print("(3.5) Pi_I C_A equals the parent conditional of Z given O: OK")

# ---- (3.6) absolute continuity ----------------------------------------
Q_A = {z: sum(Q_I[y] * C[y][z] for y in Y) for z in Z}
Pi_A = Pi_A_push[o_star]
for z in Z:
    if Pi_A[z] == 0:
        assert Q_A[z] == 0
print("(3.6) Q_A << Pi_A: OK")

# ---- (6.1)/(6.2) joint lifts and RN derivative -------------------------
Qhat = {(y, z): Q_I[y] * C[y][z] for y in Y for z in Z}
Pihat = {(y, z): Pi_I[o_star][y] * C[y][z] for y in Y for z in Z}
r = {y: Q_I[y] / Pi_I[o_star][y] for y in Y}
for (y, z) in Qhat:
    if Pihat[(y, z)] > 0:
        assert Qhat[(y, z)] / Pihat[(y, z)] == r[y], "(6.2) FAILED"
print("(6.2) dQhat/dPihat = r(Y): OK")


def KL(p, q):
    tot = 0.0
    for k in p:
        if p[k] > 0:
            if q.get(k, 0) == 0:
                return float('inf')
            tot += float(p[k]) * log(float(p[k]) / float(q[k]))
    return tot


kl_fine = KL(Q_I, Pi_I[o_star])
kl_parent = KL(Q_A, Pi_A)
# conditional disintegrations over z
Qcond = {z: {y: Qhat[(y, z)] / Q_A[z] for y in Y} for z in Z}
Picond = {z: {y: Pihat[(y, z)] / Pi_A[z] for y in Y} for z in Z}
Delta = sum(float(Q_A[z]) * KL(Qcond[z], Picond[z]) for z in Z)

print(f"    KL(Q_I||Pi_I)   = {kl_fine:.15f}")
print(f"    KL(Q_A||Pi_A)   = {kl_parent:.15f}")
print(f"    Delta_A         = {Delta:.15f}")
print(f"    residual        = {kl_fine - kl_parent - Delta:.3e}")
assert abs(kl_fine - (kl_parent + Delta)) < 1e-12, "(6.4) chain identity FAILED"
assert Delta >= 0 and kl_fine >= kl_parent
print("(6.4) KL chain identity and DPI: OK")

# ---- (6.10)/(6.11) recovery -------------------------------------------
R = Picond  # reverse kernel from the posterior lift
rec_Pi = {y: sum(Pi_A[z] * R[z][y] for z in Z) for y in Y}
assert rec_Pi == Pi_I[o_star], "(6.10) FAILED"
print("(6.10) Pi_A R = Pi_I holds for ANY channel: OK")
rec_Q = {y: sum(Q_A[z] * R[z][y] for z in Z) for y in Y}
print("(6.11) Q_A R == Q_I ?", rec_Q == Q_I,
      "(expected False here since Delta_A > 0)")

# ---- NECESSITY of the 'observation unchanged' hypothesis ---------------
# Same fine data, but now also coarsen O by the constant map phi(o) = *.
# Parent posterior given o_A = * is the Z-marginal of P_A, not Pi_I C_A.
Z_marg = {z: sum(P_A[(o, z)] for o in O) for z in Z}
print("\nNECESSITY CHECK (channel also coarsens O):")
print("   true parent posterior given o_A=*  :", {k: str(v) for k, v in Z_marg.items()})
print("   pushforward Pi_{I,a} C_A           :", {k: str(v) for k, v in Pi_A.items()})
print("   equal?", Z_marg == Pi_A,
      "-> pushforward is NOT a version when O is coarsened")
