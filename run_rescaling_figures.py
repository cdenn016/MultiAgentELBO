r"""Render the rescaling laboratory's figure suite (amendments 3-14).

Usage:  python run_rescaling_figures.py

Every panel except figure 1 and the story map is recomputed live from the
validated declared seed (the C(3,3) working-case step, checked against the
published invariants before any figure is drawn). Figure 1 carries the
audited fixed-point numbers of amendments 3-4 as recorded constants, because
regenerating the fixed points is an overnight computation; their provenance
is the 2026-08-18 audit (docs/audits/2026-08-18-rescaling-lab-audit.md),
which reproduced every one of them. Output: figures/rescaling-lab/ as PNG
(300 dpi) and PDF, with captions in the README alongside.

Figures 3C through 7 carry the republished amendments 10-14. The
lab-versus-theory audit of the same day found that the Proposition-4 block energy
charged nothing for a block's parent, which made the all-singleton partition the
exact minimizer of the cross-scale group at every configuration by construction.
With the declared top prior booked, every partition-posterior verdict in those
amendments changes, and the panels here are the re-taken ones
(docs/results/2026-08-18-amendments-10-14-republication.json).
"""

from __future__ import annotations

import math
import time
from pathlib import Path
import sys


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from multiagent_elbo.finite.categorical_falsification_model import crp_partition_prior
from multiagent_elbo.finite.cocycle_flow import (
    capacity_information_retention,
    capacity_pair_retention,
    homogeneous_circulant_instance,
    one_step_pair_retention,
)
from multiagent_elbo.finite.coupling_readback import (
    _kernel_model,
    couplings_action,
    initial_step,
)
from multiagent_elbo.finite.environmental_blocking import (
    EnvironmentalDressing,
    SharedEnvironment,
    anchored_posterior,
    dressed_instance,
    induced_pair_sup,
    shared_dressed_instance,
)
from multiagent_elbo.finite.nested_tower import build_tower_model, tower_blocks
from multiagent_elbo.finite.participatory_blocking import (
    blocking_posterior,
    cycle_blocking_candidates,
)
from multiagent_elbo.finite.partition_dynamics import (
    _evaluate_batch,
    _log_sum_exp,
    _partition_tables,
)

OKABE_ITO = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7", "#56B4E9", "#000000"]
CLASS_COLORS = {1: "#0072B2", 2: "#D55E00", 3: "#009E73", 6: "#CC79A7"}
CLASS_NAMES = {1: "singletons", 2: "ratio 2", 3: "ratio 3", 6: "direct"}
OUTPUT = Path(__file__).resolve().parent / "figures" / "rescaling-lab"

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.size": 8,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=OKABE_ITO),
        "figure.dpi": 120,
        "savefig.dpi": 300,
    }
)


def save(figure: plt.Figure, name: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT / f"{name}.png", bbox_inches="tight")
    figure.savefig(OUTPUT / f"{name}.pdf", bbox_inches="tight")
    plt.close(figure)
    print(f"  wrote {name}")


def panel_label(ax: plt.Axes, letter: str) -> None:
    ax.text(-0.12, 1.06, letter, transform=ax.transAxes, fontsize=11, fontweight="bold")


def rebuild_seed():
    tower = build_tower_model(
        3, 3, (1, 1, 0, 1, 1, 1, 0, 2, 1, 1, 2, 0), (1, 1, 1, 2, 2, 2, 0, 1, 2, 0, 1, 2)
    )
    step = initial_step(tower, (1, 0, 1, 0, 1, 0, 1, 0, 1), tower_blocks(3, 3))
    site = step.variational.sites[0]
    pair = dict(step.variational.pairs)[(0, 1)]
    site_sup = max(abs(float(v)) for v in site)
    pair_sup = max(abs(float(v)) for row in pair for v in row)
    assert abs(site_sup - 1.4321) < 5.0e-4, "seed validation failed"
    assert abs(pair_sup - 0.0163) < 5.0e-4, "seed validation failed"
    return site, pair


def annealed_classes(working) -> dict[int, float]:
    model = _kernel_model(working.graph, "figures-annealed")
    size = model.state_count
    length = len(working.graph.vertices)
    action = couplings_action(working.couplings).reshape(-1)
    declared = cycle_blocking_candidates(length)
    log_masses = []
    total = size**length
    for _, partition in declared:
        tables = _partition_tables(model, partition)
        log_terms = np.empty(total, dtype=np.float64)
        for start in range(0, total, 65536):
            stop = min(start + 65536, total)
            batch = np.array(np.unravel_index(np.arange(start, stop), (size,) * length)).T
            cross, graph, _ = _evaluate_batch(tables, batch)
            log_terms[start:stop] = -action[start:stop] - cross - graph
        log_masses.append(
            math.log(float(crp_partition_prior(partition, model.crp_concentration)))
            + float(_log_sum_exp(log_terms[None, :])[0])
        )
    weights = np.exp(np.array(log_masses) - max(log_masses))
    weights /= weights.sum()
    classes: dict[int, float] = {}
    for (ratio, _), mass in zip(declared, weights):
        classes[ratio] = classes.get(ratio, 0.0) + float(mass)
    return classes


def figure_1_passive_and_regenerated() -> None:
    """Recorded constants; provenance: 2026-08-18 audit, every number reproduced."""
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.0, 2.7))
    cuts = [1, 3, 6]
    retention = [0.156, 0.441, 0.564]
    ax_a.plot(cuts, retention, "o-", color=OKABE_ITO[0])
    ax_a.axhline(1.0, linestyle=":", color="gray", linewidth=1)
    ax_a.text(5.9, 1.02, "no attenuation", ha="right", fontsize=7, color="gray")
    ax_a.set_xlabel("cut couplings per block boundary $k$")
    ax_a.set_ylabel("one-step pair retention $R_{\\mathrm{sup}}$")
    ax_a.set_title("Passive channel: boundary thickness\ncannot rescue retention (M-bundle)")
    ax_a.set_xticks(cuts)
    ax_a.set_ylim(0, 1.1)
    panel_label(ax_a, "A")
    labels = ["passive\n(ratio 2)", "passive\n(ratio 3)", "regenerated\n(ratio 2)", "regenerated\n(ratio 3)"]
    values = [0.0, 0.0, 0.579, 0.625]
    colors = [OKABE_ITO[0], OKABE_ITO[0], OKABE_ITO[1], OKABE_ITO[1]]
    bars = ax_b.bar(labels, values, color=colors, width=0.6)
    ax_b.axhline(0.4648, linestyle="--", color="gray", linewidth=1)
    ax_b.text(3.4, 0.475, "one-step injection", ha="right", fontsize=7, color="gray")
    ax_b.annotate("machine zero", (0.5, 0.02), ha="center", fontsize=7, color=OKABE_ITO[0])
    ax_b.set_ylabel("fixed-structure pair sup")
    ax_b.set_title("Regeneration restores interaction\n(M-regen; sustained/injected 1.246)")
    ax_b.set_ylim(0, 0.72)
    panel_label(ax_b, "B")
    fig.suptitle("")
    fig.tight_layout()
    save(fig, "fig1_passive_vs_regenerated")


def figure_2_capacity(instance_k1, instance_k3) -> None:
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.0, 2.9))
    sup9, sup27, mi9, mi27, mi27_control = [], [], [], [], []
    for instance in (instance_k1, instance_k3):
        sup9.append(one_step_pair_retention(instance, 2).retention)
        sup27.append(capacity_pair_retention(instance, 2).retention)
        mi9.append(capacity_information_retention(instance, 2, sector_count=1).retention)
        mi27.append(capacity_information_retention(instance, 2, sector_count=3).retention)
        mi27_control.append(
            capacity_information_retention(
                instance, 2, sector_count=3, readout="first_member"
            ).retention
        )
    x = np.arange(2)
    width = 0.35
    ax_a.bar(x - width / 2, sup9, width, label="9-state parents", color=OKABE_ITO[0])
    ax_a.bar(x + width / 2, sup27, width, label="27 labels (root-framed)", color=OKABE_ITO[1])
    for position, value in zip((0, 1), (0.144, 0.406)):
        ax_a.hlines(value, position + width / 2 - width / 2.2, position + width / 2 + width / 2.2,
                    color="black", linestyle=":", linewidth=1.2)
    ax_a.plot([], [], ":", color="black", label="retired (gauge-variant charge)")
    ax_a.set_xticks(x, ["$k=1$", "$k=3$"])
    ax_a.set_ylabel("$R_{\\mathrm{sup}}$")
    ax_a.set_title("Coupling units: the sup norm\n(sector gain +34% / +29%)")
    ax_a.legend(frameon=False, loc="upper left")
    panel_label(ax_a, "A")
    third = 0.27
    ax_b.bar(x - third, mi9, third, label="9-state parents", color=OKABE_ITO[0])
    ax_b.bar(x, mi27, third, label="27 labels: gauge charge", color=OKABE_ITO[1])
    ax_b.bar(x + third, mi27_control, third,
             label="27 labels: first-member control", color=OKABE_ITO[3])
    for position, (s9,) in zip((0, 1), zip(sup9)):
        ax_b.hlines(s9**2, position - width, position + width, color="gray",
                    linestyle="--", linewidth=1)
    ax_b.plot([], [], "--", color="gray", label="$R_{\\mathrm{sup}}^2$ (square-law check)")
    ax_b.set_xticks(x, ["$k=1$", "$k=3$"])
    ax_b.set_ylabel("$R_{\\mathrm{MI}}$")
    ax_b.set_title("Law units: any refinement raises $R_{\\mathrm{MI}}$;\n"
                   "a non-charge readout raises it more")
    ax_b.legend(frameon=False, loc="upper left")
    panel_label(ax_b, "B")
    fig.tight_layout()
    save(fig, "fig2_capacity_two_instruments")


def figure_3_coupling_sweep(site, pair) -> None:
    from fractions import Fraction

    grid = [1, 3, 10, 30, 100]
    ceilings, r_mi, r_sup, class_masses = [], [], [], []
    for scale in grid:
        scaled = tuple(tuple(v * Fraction(scale) for v in row) for row in pair)
        instance = homogeneous_circulant_instance(6, (1,), site, scaled)
        info = capacity_information_retention(instance, 2, sector_count=1)
        ceilings.append(info.fine_information)
        r_mi.append(info.retention)
        r_sup.append(one_step_pair_retention(instance, 2).retention)
        class_masses.append(dict(blocking_posterior(instance).class_masses))
    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(9.5, 2.8))
    ax_a.loglog(grid, ceilings, "o-", color=OKABE_ITO[0], label="measured")
    guide = [ceilings[0] * (g / grid[0]) ** 2 for g in grid]
    ax_a.loglog(grid, guide, "--", color="gray", label="$\\lambda^2$ guide")
    ax_a.set_xlabel("coupling scale $\\lambda$")
    ax_a.set_ylabel("$I(X_{B_1};X_{B_2})$ (nats)")
    ax_a.set_title("The ceiling grows as $\\lambda^2$")
    ax_a.legend(frameon=False)
    panel_label(ax_a, "A")
    ax_b.semilogx(grid, r_sup, "o-", color=OKABE_ITO[0], label="$R_{\\mathrm{sup}}$")
    ax_b.semilogx(grid, r_mi, "s-", color=OKABE_ITO[1], label="$R_{\\mathrm{MI}}$")
    ax_b.set_xlabel("coupling scale $\\lambda$")
    ax_b.set_ylabel("retention")
    ax_b.set_title("Transmission is kernel-limited,\nnot signal-limited")
    ax_b.set_ylim(0, 0.5)
    ax_b.legend(frameon=False)
    panel_label(ax_b, "B")
    for ratio in (1, 2, 3, 6):
        ax_c.semilogx(grid, [c[ratio] for c in class_masses], "o-",
                      color=CLASS_COLORS[ratio], label=CLASS_NAMES[ratio])
    ax_c.set_xlabel("coupling scale $\\lambda$")
    ax_c.set_ylabel("partition class mass")
    ax_c.set_title("Direct aggregation modal at every $\\lambda$\n"
                   "(M-bind; couplings act only through the flow)")
    ax_c.set_ylim(0, 1.02)
    ax_c.legend(frameon=False, ncols=2)
    panel_label(ax_c, "C")
    fig.tight_layout()
    save(fig, "fig3_coupling_sweep")


def figure_4_anchors(instance) -> None:
    patterns = {
        "uniform anchors\n(0,0,0,0,0,0)": (0, 0, 0, 0, 0, 0),
        "shared pairs\n(0,0,4,4,8,8)": (0, 0, 4, 4, 8, 8),
        "distinct control\n(0,1,2,3,4,5)": (0, 1, 2, 3, 4, 5),
    }
    strengths = [0.5, 2.0, 8.0]
    fig, axes = plt.subplots(1, 3, figsize=(9.5, 2.8), sharey=True)
    for ax, (title, pinned), letter in zip(axes, patterns.items(), "ABC"):
        masses = {ratio: [] for ratio in (1, 2, 3, 6)}
        for strength in strengths:
            posterior = anchored_posterior(
                instance, EnvironmentalDressing(pinned=pinned, strength=strength)
            )
            for ratio, mass in posterior.class_masses:
                masses[ratio].append(mass)
        for ratio in (1, 2, 3, 6):
            ax.semilogx(strengths, masses[ratio], "o-", color=CLASS_COLORS[ratio],
                        label=CLASS_NAMES[ratio])
        ax.set_xlabel("anchor strength $\\kappa_{\\mathrm{env}}$")
        ax.set_title(title)
        ax.set_ylim(0, 1.0)
        panel_label(ax, letter)
    axes[0].set_ylabel("partition class mass")
    axes[0].legend(frameon=False)
    fig.suptitle("M-anchor: shared evidence moves mass toward the aligned blocking,\n"
                 "but direct aggregation stays modal throughout", y=1.08, fontsize=10)
    fig.tight_layout()
    save(fig, "fig4_environmental_anchors")


def figure_5_process_vs_landscape(instance) -> None:
    dressing = EnvironmentalDressing(pinned=(0, 0, 4, 4, 8, 8), strength=2.0)
    cases = {
        "bare instance": (
            dict(blocking_posterior(instance).class_masses),
            annealed_classes(instance),
        ),
        "shared-pair anchors ($\\kappa_{\\mathrm{env}}=2$)": (
            dict(anchored_posterior(instance, dressing).class_masses),
            annealed_classes(dressed_instance(instance, dressing)),
        ),
    }
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), sharey=True)
    width = 0.35
    x = np.arange(4)
    ratios = (1, 2, 3, 6)
    for ax, (title, (quenched, annealed)), letter in zip(axes, cases.items(), "AB"):
        ax.bar(x - width / 2, [quenched[r] for r in ratios], width,
               label="quenched (landscape)", color=OKABE_ITO[0])
        ax.bar(x + width / 2, [annealed[r] for r in ratios], width,
               label="annealed (process)", color=OKABE_ITO[1])
        ax.set_xticks(x, [CLASS_NAMES[r] for r in ratios])
        ax.set_title(title)
        panel_label(ax, letter)
    axes[0].set_ylabel("partition class mass")
    axes[0].legend(frameon=False)
    fig.suptitle("M-flow: the process agrees with the landscape once the parent is priced",
                 y=1.04, fontsize=10)
    fig.tight_layout()
    save(fig, "fig5_process_vs_landscape")


def figure_6_saturation_and_inertia(instance) -> None:
    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(9.5, 2.8))
    strengths = [8.0, 16.0, 32.0, 64.0, 128.0]
    aligned_q = []
    for strength in strengths:
        posterior = anchored_posterior(
            instance, EnvironmentalDressing(pinned=(0, 0, 4, 4, 8, 8), strength=strength)
        )
        aligned_q.append(dict(zip(posterior.candidates, posterior.masses)).get(
            ((1, 2), (3, 4), (5, 6)), 0.0))
    ax_a.semilogx(strengths, aligned_q, "o-", color=OKABE_ITO[0])
    ax_a.axhline(0.038816, linestyle="--", color="gray", linewidth=1)
    ax_a.text(120, 0.0392, "frozen limit", ha="right", fontsize=7, color="gray")
    ax_a.set_xlabel("anchor strength $\\kappa_{\\mathrm{env}}$")
    ax_a.set_ylabel("aligned-placement mass")
    ax_a.set_title("Pinning saturates before condensing\n(M-cross-env)")
    ax_a.set_ylim(0.0384, 0.0396)
    panel_label(ax_a, "A")
    inertias = [0.0, 1.0, 4.0, 16.0, 64.0]
    shared_masses, control_masses, pair_sups = [], [], []
    for inertia in inertias:
        shared = SharedEnvironment(
            groups=((1, 2), (3, 4), (5, 6)), preferred=(0, 4, 8),
            strength=8.0, inertia=inertia,
        )
        posterior = blocking_posterior(shared_dressed_instance(instance, shared))
        shared_masses.append(dict(zip(posterior.candidates, posterior.masses)).get(
            ((1, 2), (3, 4), (5, 6)), 0.0))
        pair_sups.append(induced_pair_sup(instance, shared))
        control = SharedEnvironment(
            groups=tuple((s,) for s in range(1, 7)), preferred=(0, 0, 4, 4, 8, 8),
            strength=8.0, inertia=inertia,
        )
        control_posterior = blocking_posterior(shared_dressed_instance(instance, control))
        control_masses.append(dict(zip(control_posterior.candidates,
                                       control_posterior.masses)).get(
            ((1, 2), (3, 4), (5, 6)), 0.0))
    positions = [max(m, 0.25) for m in inertias]
    ax_b.semilogx(positions, shared_masses, "o-", color=OKABE_ITO[1],
                  label="shared agents")
    ax_b.semilogx(positions, control_masses, "s--", color=OKABE_ITO[0],
                  label="private duplicates")
    ax_b.axhline(0.039236, linestyle=":", color="gray", linewidth=1)
    ax_b.text(60, 0.0400, "pinned limit", ha="right", fontsize=7, color="gray")
    ax_b.set_xticks(positions, ["0", "1", "4", "16", "64"])
    ax_b.set_xlabel("environmental inertia $m$")
    ax_b.set_ylabel("aligned-placement mass")
    ax_b.set_title("Sharing beats duplicating at low inertia;\nalignment wins overall (M-share)")
    ax_b.legend(frameon=False, loc="lower right")
    panel_label(ax_b, "B")
    ax_c.semilogx(positions, pair_sups, "o-", color=OKABE_ITO[2])
    ax_c.set_xticks(positions, ["0", "1", "4", "16", "64"])
    ax_c.set_xlabel("environmental inertia $m$")
    ax_c.set_ylabel("induced pair sup")
    ax_c.set_title("The correlation channel vanishes\nas the environment freezes")
    panel_label(ax_c, "C")
    fig.tight_layout()
    save(fig, "fig6_saturation_and_inertia")


def figure_7_story() -> None:
    entries = [
        ("M-bundle / fixed points", "passive channel trivial;\nboundary thickness cannot rescue", "#0072B2"),
        ("M-regen (amendment 4)", "regenerated attention sustains\ninteracting fixed structures", "#009E73"),
        ("Audit F8 + amendment 8", "gauge-variant sector charge retired;\ncapacity null reverses (0.144 to 0.209)", "#D55E00"),
        ("M-info (amendment 9)", "R_MI <= 1 is a theorem; the gain's sign\nis too, so a non-charge control decides", "#D55E00"),
        ("Audit finding 1 (2026-08-18)", "the parent was free; priced by the\ndeclared top prior, 10-14 re-taken", "#CC79A7"),
        ("M-part (amendment 10)", "offered the choice, the posterior\naggregates: direct modal (0.958)", "#D55E00"),
        ("M-bind (amendment 11)", "direct modal at every lambda; couplings\nreach the flow, never the landscape", "#D55E00"),
        ("M-anchor (amendment 12)", "shared evidence moves mass 32x toward\nthe aligned pairing, no modal flip", "#009E73"),
        ("M-flow (amendment 12)", "quenched and annealed now agree;\nthe reversal was a free-parent artifact", "#D55E00"),
        ("M-cross-env (amendment 13)", "point-mass environments align\nbut cannot correlate (plateau 0.0388)", "#0072B2"),
        ("M-share (amendment 14)", "alignment and correlation compete;\nalignment wins at this seed (5.6x)", "#0072B2"),
    ]
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    ax.axis("off")
    for index, (title, verdict, color) in enumerate(entries):
        y = 1.0 - index / len(entries)
        ax.add_patch(plt.Rectangle((0.02, y - 0.085), 0.30, 0.082,
                                   facecolor=color, alpha=0.15, edgecolor=color))
        ax.text(0.17, y - 0.044, title, ha="center", va="center",
                fontsize=8, fontweight="bold", color=color)
        ax.text(0.36, y - 0.044, verdict, ha="left", va="center", fontsize=8)
        if index < len(entries) - 1:
            ax.annotate("", xy=(0.17, y - 0.093), xytext=(0.17, y - 0.085),
                        arrowprops=dict(arrowstyle="-|>", color="gray"))
    ax.text(0.5, 1.06, "The rescaling laboratory, 2026-08-17/18: measurement chain and verdicts",
            ha="center", fontsize=10, fontweight="bold", transform=ax.transAxes)
    ax.text(0.5, 1.025,
            "amendments 10-14 republished 2026-08-18 after the lab-versus-theory audit",
            ha="center", fontsize=7.5, color="#555555", transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.02, 1.02)
    save(fig, "fig7_story_map")


def main() -> None:
    started = time.perf_counter()
    print("rebuilding the validated seed...")
    site, pair = rebuild_seed()
    instance_k1 = homogeneous_circulant_instance(6, (1,), site, pair)
    instance_k3 = homogeneous_circulant_instance(6, (1, 2), site, pair)
    print("figure 1 (recorded constants)...")
    figure_1_passive_and_regenerated()
    print("figure 2 (capacity, live)...")
    figure_2_capacity(instance_k1, instance_k3)
    print("figure 3 (coupling sweep, live)...")
    figure_3_coupling_sweep(site, pair)
    print("figure 4 (anchors, live)...")
    figure_4_anchors(instance_k1)
    print("figure 5 (process vs landscape, live)...")
    figure_5_process_vs_landscape(instance_k1)
    print("figure 6 (saturation and inertia, live)...")
    figure_6_saturation_and_inertia(instance_k1)
    print("figure 7 (story map)...")
    figure_7_story()
    print(f"done in {time.perf_counter() - started:.0f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()
