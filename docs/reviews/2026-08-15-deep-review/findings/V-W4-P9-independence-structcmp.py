"""Independent structural comparison: direct-derivation.md vs independent-reconstruction.md.

(1) reproduce the wave-1 n-gram overlap numbers
(2) enumerate admissible SECTION-BLOCK orders under the frozen dependency DAG
"""
import re, json, itertools

BASE = ("C:/Users/chris and christine/Desktop/MultiAgentELBO/docs/derivations/"
        "2026-08-15-full-pointwise-meta-agent/")

def toks(path):
    t = open(BASE + "evidence/" + path, encoding="utf-8").read().lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return t.split()

d = toks("direct-derivation.md")
r = toks("independent-reconstruction.md")

print("token counts: direct=%d recon=%d" % (len(d), len(r)))
for n in (4, 5, 6, 8):
    D = set(tuple(d[i:i+n]) for i in range(len(d)-n+1))
    R = [tuple(r[i:i+n]) for i in range(len(r)-n+1)]
    Rs = set(R)
    shared = Rs & D
    print("n=%d: recon distinct %d-grams=%4d shared=%3d (%.1f%%)"
          % (n, n, len(Rs), len(shared), 100*len(shared)/len(Rs)))
    if n == 8:
        for g in sorted(shared):
            print("      8-gram:", " ".join(g))

# ---- block-order enumeration ----
dag = json.load(open(BASE + "dependency-dag.json", encoding="utf-8"))
prereq = {}
for e in dag["edges"]:
    prereq.setdefault(e["from"], set()).add(e["to"])

block = {
    "A": ["POINTWISE-TYPING", "PARENT-NORMALIZATION", "POSTERIOR-PUSHFORWARD",
          "COMMON-CHANNEL-ABSOLUTE-CONTINUITY"],
    "B": ["MODEL-FAMILY-NORMALIZATION", "EVALUATION-COMPATIBILITY"],
    "C": ["DERIVED-MARGINALS"],
    "D": ["VFE-CHAIN-EXTENDED", "VFE-FINITE-ZERO-DEFECT-RECOVERY"],
    "E": ["HOLONOMY-BLIND-FULL-LAW", "HOLONOMY-RETENTION", "HOLONOMY-ALTERNATIVE"],
    "F": ["DYNAMICS-SCOPE"],
    "G": ["NEG-MARGINAL-DETERMINATION", "NEG-SPLIT-CHANNEL-VFE",
          "NEG-MODEL-MARGINAL-EVALUATION", "NEG-TRIVIAL-HOLONOMY-AGREEMENT",
          "NEG-MARGINAL-HOLONOMY-JOINT"],
}
owner = {n: b for b, ns in block.items() for n in ns}

# cross-block precedences forced by the DAG
cross = set()
for a, deps in prereq.items():
    if a == "target" or a not in owner:
        continue
    for b in deps:
        if b in owner and owner[b] != owner[a]:
            cross.add((owner[b], owner[a]))   # b's block before a's block
print("\nforced cross-block precedences:", sorted(cross))

names = list(block)
ok = [p for p in itertools.permutations(names)
      if all(p.index(x) < p.index(y) for x, y in cross)]
print("admissible block orders (7 blocks incl. counterexamples):", len(ok))

names2 = [b for b in names if b != "G"]
cross2 = {(x, y) for x, y in cross if x != "G" and y != "G"}
ok2 = [p for p in itertools.permutations(names2)
       if all(p.index(x) < p.index(y) for x, y in cross2)]
print("admissible block orders, affirmative blocks only (A..F):", len(ok2))
print("order actually used by BOTH documents (affirmative part): ('A','B','C','D','E','F')")
print("is it admissible:", ("A","B","C","D","E","F") in ok2)
