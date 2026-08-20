r"""Amendment 10: participatory blocking, the flow selecting its own partition.

Every blocking so far was declared data. This module lets the theory's own
selection mechanism choose it: at each level the Proposition-4 partition
posterior $Q_R(R) \propto P_R(R)\, e^{-\bar U(R)}$ is evaluated over the
declared cycle-blocking candidates, with $\bar U(R) = \mathbb E_w[U(R, x)]$
the flow-averaged derived block energy — Proposition 4 with the point-mass
child recognition law replaced by the level's Boltzmann flow, which shifts
every candidate by the same flow entropy and therefore leaves the Gibbs law
untouched. The realized step blocks by the modal ratio class through the
audited read-back route and iterates until the modal class is the singleton
partition or one site remains. Nothing here proposes an energy: $U$ is the
M5 module's derived sum of conditional divergences, evaluated on the
level-invariant kernel model of the instance's graph, and the prior is the
declared Ewens law, temperature one, untempered.

Two scopes the 2026-08-18 lab-versus-theory audit fixed on this route, both
of which change what a sweep here can be read as measuring. First, the block
energy charges the declared top prior for each block's parent, so opening a
block costs something; before 2026-08-18 it did not, and the all-singleton
partition was the exact minimizer of the cross-scale group at every
configuration by construction rather than by measurement. Second, the
instance's couplings never enter $U$ — the kernel model is level-invariant
declared structure — so they act only through the flow $w$. A coupling-scale
sweep is a reweighting of the configurations the energy is averaged over, and
it cannot move the landscape; no coupling magnitude can, and that is a
structural fact about the construction rather than a measured absence of a
transition. The Ewens concentration is likewise a declared knob and is now a
parameter of this route rather than a hardwired one.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from fractions import Fraction

from .categorical_falsification_model import Partition, crp_partition_prior
from .cocycle_flow import consecutive_blocks, regenerated_instance
from .coupling_readback import (
    DECLARED_CONCENTRATION,
    PairwiseInstance,
    _kernel_model,
    couplings_action,
    iterated_step,
)
from .partition_dynamics import _evaluate_batch, _partition_tables

_BATCH_SIZE = 65536


def cycle_blocking_candidates(length: int) -> tuple[tuple[int, Partition], ...]:
    """Return the declared (ratio, partition) candidates of one cycle length.

    The singleton partition carries ratio one; every divisor ratio in
    [2, length] contributes its consecutive blockings in every rotational
    placement (ratio placements for a proper divisor, one for the direct
    single block), with wrapped blocks counted as consecutive on the cycle.
    """
    if type(length) is not int or length < 2:
        raise ValueError("a blocking candidate set needs at least two sites")
    candidates: list[tuple[int, Partition]] = [
        (1, tuple((site,) for site in range(1, length + 1)))
    ]
    for ratio in range(2, length + 1):
        if length % ratio != 0:
            continue
        placements = 1 if ratio == length else ratio
        for offset in range(placements):
            blocks = []
            for start in range(0, length, ratio):
                blocks.append(
                    tuple(
                        sorted(
                            (start + offset + position) % length + 1
                            for position in range(ratio)
                        )
                    )
                )
            candidates.append((ratio, tuple(sorted(blocks))))
    return tuple(candidates)


@dataclass(frozen=True)
class BlockingPosterior:
    """The Proposition-4 posterior over one level's blocking candidates.

    concentration records the Ewens concentration the posterior was taken
    at, because the verdict is not concentration-free: the modal class of the
    declared 6-cycle instances crosses inside the unit interval, so a posterior
    reported without its concentration reports a point on a surface as if it
    were the surface.
    """

    length: int
    candidates: tuple[Partition, ...]
    ratios: tuple[int, ...]
    energies: tuple[float, ...]
    log_priors: tuple[float, ...]
    masses: tuple[float, ...]
    class_masses: tuple[tuple[int, float], ...]
    modal_ratio: int
    placement_gap: float
    concentration: Fraction = DECLARED_CONCENTRATION


@dataclass(frozen=True)
class ParticipatoryLevel:
    """One level of the participatory flow: the posterior and the step taken."""

    length: int
    posterior: BlockingPosterior
    chosen: Partition | None


@dataclass(frozen=True)
class ParticipatoryPath:
    """The realized participatory flow of one instance in one channel."""

    channel: str
    levels: tuple[ParticipatoryLevel, ...]
    site_counts: tuple[int, ...]


def blocking_posterior(
    instance: PairwiseInstance,
    concentration: Fraction = DECLARED_CONCENTRATION,
) -> BlockingPosterior:
    r"""Return the partition posterior of one level under its own flow.

    The block energy of each candidate is $\bar U(R) = \sum_x w(x) U(R, x)$
    with $w$ the normalized Boltzmann flow of the instance's coupling action
    and $U$ the derived Proposition-4 energy on the level-invariant kernel
    model; the posterior weight is $\log P_{\mathrm{Ewens}}(R) - \bar U(R)$,
    normalized over the declared candidates. The placement gap is the largest
    within-class mass spread, which homogeneity requires to vanish.

    ``concentration`` is the Ewens concentration of the block-count prior.
    It is the one genuinely free parameter of the selection, it was pinned at
    one and unreachable from this route until 2026-08-18, and the declared
    instances sit close enough to a crossing that a single-point report is not
    a result; :func:`concentration_surface` reports it as a surface.

    The instance's couplings do not enter the block energy. They enter only
    through the flow, so a coupling-scale sweep reweights the configurations
    the energy is averaged over and never moves the landscape itself.
    """
    length = len(instance.graph.vertices)
    model = _kernel_model(instance.graph, "participatory-blocking", concentration)
    size = model.state_count
    action = couplings_action(instance.couplings)
    weights = np.exp(-(action - action.min())).reshape(-1)
    weights = weights / weights.sum()
    total = size**length
    declared = cycle_blocking_candidates(length)
    energies: list[float] = []
    log_priors: list[float] = []
    for _, partition in declared:
        tables = _partition_tables(model, partition)
        averaged = 0.0
        for start in range(0, total, _BATCH_SIZE):
            stop = min(start + _BATCH_SIZE, total)
            batch = np.array(
                np.unravel_index(np.arange(start, stop), (size,) * length)
            ).T
            cross, graph, _ = _evaluate_batch(tables, batch)
            averaged += float(np.dot(weights[start:stop], cross + graph))
        energies.append(averaged)
        log_priors.append(
            math.log(float(crp_partition_prior(partition, model.crp_concentration)))
        )
    scores = np.array(log_priors) - np.array(energies)
    masses = np.exp(scores - scores.max())
    masses = masses / masses.sum()
    classes: dict[int, float] = {}
    spreads: dict[int, list[float]] = {}
    for (ratio, _), mass in zip(declared, masses):
        classes[ratio] = classes.get(ratio, 0.0) + float(mass)
        spreads.setdefault(ratio, []).append(float(mass))
    placement_gap = max(
        (max(values) - min(values) for values in spreads.values()),
        default=0.0,
    )
    modal_ratio = max(classes, key=classes.get)
    return BlockingPosterior(
        length=length,
        candidates=tuple(partition for _, partition in declared),
        ratios=tuple(ratio for ratio, _ in declared),
        energies=tuple(energies),
        log_priors=tuple(log_priors),
        masses=tuple(float(value) for value in masses),
        class_masses=tuple(sorted(classes.items())),
        modal_ratio=modal_ratio,
        placement_gap=placement_gap,
        concentration=Fraction(concentration),
    )


@dataclass(frozen=True)
class ConcentrationSurface:
    """The modal class of one level's partition posterior across concentrations.

    The Ewens prior's concentration is the free parameter of the selection, and
    the declared instances do not sit far from a crossing in it, so the honest
    published object is this surface rather than the single point at the
    declared concentration. ``crossings`` names each adjacent pair of swept
    concentrations whose modal classes differ, which brackets every crossing on
    the swept grid.
    """

    concentrations: tuple[Fraction, ...]
    modal_ratios: tuple[int, ...]
    class_masses: tuple[tuple[tuple[int, float], ...], ...]
    crossings: tuple[tuple[Fraction, Fraction, int, int], ...]


def concentration_surface(
    instance: PairwiseInstance,
    concentrations: Sequence[Fraction],
) -> ConcentrationSurface:
    """Return the partition posterior of one level across a concentration grid.

    Every point is an exact posterior, computed by the same route as the
    single-point report; only the block-count prior's concentration moves. The
    block energies are concentration-independent, so this is a re-weighting of
    one computed energy vector rather than a re-measurement, but it is computed
    honestly per point rather than assumed.
    """
    swept = tuple(Fraction(value) for value in concentrations)
    if not swept:
        raise ValueError("a concentration surface needs at least one point")
    posteriors = tuple(blocking_posterior(instance, value) for value in swept)
    modal = tuple(posterior.modal_ratio for posterior in posteriors)
    crossings = tuple(
        (swept[index], swept[index + 1], modal[index], modal[index + 1])
        for index in range(len(swept) - 1)
        if modal[index] != modal[index + 1]
    )
    return ConcentrationSurface(
        concentrations=swept,
        modal_ratios=modal,
        class_masses=tuple(posterior.class_masses for posterior in posteriors),
        crossings=crossings,
    )


def participatory_flow(
    instance: PairwiseInstance,
    channel: str = "regenerated",
) -> ParticipatoryPath:
    """Run the participatory flow: each level blocks by its own modal class.

    The realized step uses the lexicographically first placement of the modal
    ratio (licensed by the measured placement symmetry) through the audited
    read-back route; the regenerated channel re-binds attention per level by
    the amendment-4 rule, the passive channel inherits the read-back
    couplings unchanged. The flow stops when the modal class is the singleton
    partition or one site remains.
    """
    if channel not in ("regenerated", "passive"):
        raise ValueError("channel must be regenerated or passive")
    levels: list[ParticipatoryLevel] = []
    site_counts: list[int] = [len(instance.graph.vertices)]
    current: PairwiseInstance | None = instance
    while current is not None and len(current.graph.vertices) >= 2:
        posterior = blocking_posterior(current)
        if posterior.modal_ratio == 1:
            levels.append(
                ParticipatoryLevel(
                    length=posterior.length, posterior=posterior, chosen=None
                )
            )
            break
        chosen = consecutive_blocks(posterior.length, posterior.modal_ratio)
        levels.append(
            ParticipatoryLevel(
                length=posterior.length, posterior=posterior, chosen=chosen
            )
        )
        step = iterated_step(current, chosen)
        site_counts.append(len(chosen))
        if step.instance is None:
            current = None
        elif channel == "regenerated":
            current = regenerated_instance(step).instance
        else:
            current = step.instance
    return ParticipatoryPath(
        channel=channel,
        levels=tuple(levels),
        site_counts=tuple(site_counts),
    )


__all__ = [
    "BlockingPosterior",
    "ConcentrationSurface",
    "ParticipatoryLevel",
    "ParticipatoryPath",
    "blocking_posterior",
    "concentration_surface",
    "cycle_blocking_candidates",
    "participatory_flow",
]
