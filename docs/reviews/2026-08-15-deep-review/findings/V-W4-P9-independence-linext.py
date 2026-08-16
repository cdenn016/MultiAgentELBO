"""Count linear extensions of the frozen dependency DAG.

Settles whether the derivation order shared by direct-derivation.md and
independent-reconstruction.md is FORCED by the dependency structure
(number of linear extensions == 1) or CONTINGENT (many extensions).
"""
import json
import itertools
from functools import lru_cache

PATH = ("C:/Users/chris and christine/Desktop/MultiAgentELBO/docs/derivations/"
        "2026-08-15-full-pointwise-meta-agent/dependency-dag.json")

dag = json.load(open(PATH, encoding="utf-8"))
# edge {"from": A, "to": B} means A depends on B, so B must be proved BEFORE A.
prereq = {}
nodes = set()
for e in dag["edges"]:
    a, b = e["from"], e["to"]
    nodes.add(a); nodes.add(b)
    prereq.setdefault(a, set()).add(b)
for n in nodes:
    prereq.setdefault(n, set())

# Closure of `target` minus target itself.
def ancestors(root):
    seen = set()
    stack = [root]
    while stack:
        x = stack.pop()
        for y in prereq[x]:
            if y not in seen:
                seen.add(y); stack.append(y)
    return seen

closure = ancestors("target")
print("closure size (excluding target):", len(closure))
print(sorted(closure))

idx = {n: i for i, n in enumerate(sorted(closure))}
N = len(idx)
pre_mask = [0] * N
for n, i in idx.items():
    m = 0
    for p in prereq[n]:
        if p in idx:
            m |= 1 << idx[p]
    pre_mask[i] = m

@lru_cache(maxsize=None)
def count(done):
    if done == (1 << N) - 1:
        return 1
    tot = 0
    for i in range(N):
        if not (done >> i) & 1 and (pre_mask[i] & done) == pre_mask[i]:
            tot += count(done | (1 << i))
    return tot

total = count(0)
print("linear extensions of the target closure:", total)

# Also: restricted to the 9 affirmative (non-NEG) nodes only.
aff = {n for n in closure if not n.startswith("NEG-")}
idx2 = {n: i for i, n in enumerate(sorted(aff))}
N2 = len(idx2)
pre2 = [0] * N2
for n, i in idx2.items():
    m = 0
    for p in prereq[n]:
        if p in idx2:
            m |= 1 << idx2[p]
    pre2[i] = m

@lru_cache(maxsize=None)
def count2(done):
    if done == (1 << N2) - 1:
        return 1
    tot = 0
    for i in range(N2):
        if not (done >> i) & 1 and (pre2[i] & done) == pre2[i]:
            tot += count2(done | (1 << i))
    return tot

print("affirmative-only nodes:", N2, sorted(aff))
print("linear extensions, affirmative closure only:", count2(0))

# Specific question: is VFE-CHAIN-EXTENDED forced to come AFTER
# EVALUATION-COMPATIBILITY / DERIVED-MARGINALS?  Check comparability.
def reach(n):
    seen = set(); stack = [n]
    while stack:
        x = stack.pop()
        for y in prereq.get(x, ()):
            if y not in seen:
                seen.add(y); stack.append(y)
    return seen

pairs = [
    ("VFE-CHAIN-EXTENDED", "EVALUATION-COMPATIBILITY"),
    ("VFE-CHAIN-EXTENDED", "DERIVED-MARGINALS"),
    ("VFE-FINITE-ZERO-DEFECT-RECOVERY", "EVALUATION-COMPATIBILITY"),
    ("VFE-FINITE-ZERO-DEFECT-RECOVERY", "DERIVED-MARGINALS"),
    ("HOLONOMY-RETENTION", "EVALUATION-COMPATIBILITY"),
    ("HOLONOMY-RETENTION", "VFE-CHAIN-EXTENDED"),
    ("DERIVED-MARGINALS", "EVALUATION-COMPATIBILITY"),
    ("COMMON-CHANNEL-ABSOLUTE-CONTINUITY", "MODEL-FAMILY-NORMALIZATION"),
    ("HOLONOMY-BLIND-FULL-LAW", "VFE-CHAIN-EXTENDED"),
]
print("\nOrder-comparability of section-level pairs (incomparable => order is a free choice):")
for a, b in pairs:
    ab = b in reach(a)
    ba = a in reach(b)
    rel = "A after B (forced)" if ab else ("B after A (forced)" if ba else "INCOMPARABLE (free)")
    print(f"  {a:38s} vs {b:32s} -> {rel}")
