"""Wave-2 skeptic reconstruction of the P1-High-3 null-slice counterexample.

All spaces are finite, so every KL is an exact finite sum. The only
measure-theoretic content -- that changing the rcp on the Lebesgue-null set
{1/2} leaves identity (1.1) intact -- is argued analytically in
V-P1-High-3-null-slice.md section 1, not here.

Run: python V-P1-High-3-null-slice-check.py   (no torch; CPU interpreter is fine)
"""
from math import log


def kl(q, p):
    """KL(q || p) for dicts over a common finite alphabet, extended-valued."""
    total = 0.0
    for y, qy in q.items():
        if qy == 0.0:
            continue
        py = p.get(y, 0.0)
        if py == 0.0:
            return float("inf")
        total += qy * log(qy / py)
    return total


print("=== Part 1: investigator's exhibited example, Y_I = {0,1} ===")
Q = {0: 1.0, 1: 0.0}                     # delta_0
PiA = {0: 0.5, 1: 0.5}                   # Version A at o=1/2 : Ber(1/2)
PiB = {0: 1.0, 1: 0.0}                   # Version B at o=1/2 : delta_0
pX_at_o = 1.0                            # p_X == 1 on [0,1], so -log p_X(o) = 0
print("  F_I under Version A =", -log(pX_at_o) + kl(Q, PiA), " (log 2 =", log(2), ")")
print("  F_I under Version B =", -log(pX_at_o) + kl(Q, PiB))
print("  Q << Pi^A ?", all(Q[y] == 0 or PiA[y] > 0 for y in Q))
print("  Q << Pi^B ?", all(Q[y] == 0 or PiB[y] > 0 for y in Q))

print()
print("=== Part 2: the claimed range [0, infinity] ===")
for eps in [0.0, 0.25, 0.5, 0.9, 0.99, 0.999999]:
    Pi_eps = {0: 1.0 - eps, 1: eps}
    print("  eps=%-10s KL(delta_0||Ber(eps)) = %-20s  Q<<Pi: %s"
          % (eps, kl(Q, Pi_eps), Pi_eps[0] > 0))
Pi_one = {0: 0.0, 1: 1.0}
print("  eps=1.0        KL =", kl(Q, Pi_one),
      " Q<<Pi:", Pi_one[0] > 0, "  <-- violates premise (1.2) Q << Pi")

print()
print("=== Part 3: is the DEFECT Delta_A itself version dependent? ===")
# Y_I = {0,1}^2, Z_A = {0,1}, C_A = projection onto the first coordinate
# (deterministic, hence a legitimate normalized measurable Markov kernel).
Ys = [(0, 0), (0, 1), (1, 0), (1, 1)]


def push(law):
    out = {0: 0.0, 1: 0.0}
    for (a, _b), m in law.items():
        out[a] += m
    return out


def defect(Qi, Pii):
    """Delta_A: expected conditional KL of the discarded coordinate under Q_A, per (6.4)."""
    QA, PA = push(Qi), push(Pii)
    total = 0.0
    for a in (0, 1):
        if QA[a] == 0.0:
            continue
        if PA[a] == 0.0:
            return float("inf")
        qc = {b: Qi[(a, b)] / QA[a] for b in (0, 1)}
        pc = {b: Pii[(a, b)] / PA[a] for b in (0, 1)}
        total += QA[a] * kl(qc, pc)
    return total


Q2 = {(0, 0): 0.5, (0, 1): 0.0, (1, 0): 0.0, (1, 1): 0.5}     # uniform on diagonal
PiA2 = {(0, 0): .25, (0, 1): .25, (1, 0): .25, (1, 1): .25}   # Version A: product
PiB2 = {(0, 0): 0.5, (0, 1): 0.0, (1, 0): 0.0, (1, 1): 0.5}   # Version B at o=1/2
for name, Pi in (("A (product)", PiA2), ("B (diagonal)", PiB2)):
    ac = all(Q2[y] == 0 or Pi[y] > 0 for y in Ys)
    print("  Version %-13s KL_fine=%-8.6f KL_coarse=%-8.6f Delta_A=%-8.6f  Q<<Pi:%s"
          % (name, kl(Q2, Pi), kl(push(Q2), push(Pi)), defect(Q2, Pi), ac))
