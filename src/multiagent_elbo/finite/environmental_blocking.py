r"""Amendment 12: the environment as a blockable agent class, and coupled descent.

Under the agent-only ontology an observation is a coupling to an environmental
agent — an agent of effectively infinite belief inertia — and such agents block
like everything else rather than being integrated out at the fine level. The
dressing of a level is one pinned state per site with a declared strength; the
environmental agent shares its site's frame (identity transport) and
contributes the two-channel divergence site field
$F_a(x) = \kappa_{\mathrm{env}}[\mathrm{KL}(b_x \| b_{\epsilon_a}) +
\mathrm{KL}(m_x \| m_{\epsilon_a})]$. Dressing adds the anchored field to the
site tables, so a dressed level rides every audited instrument unchanged; under
blocking the environment blocks too, its coarse pin the Bayes-optimal parent of
its pinned children under the declared downward kernels — the point-mass limit
of the audited kernel — and undressing subtracts the declared coarse field from
the read-back's site sector, exactly, because the field is a site function.
Environmental agents are not partition members; they enter the partition
posterior through the flow they reshape.

The coupled-descent instrument runs the theory's process rather than its
landscape: joint Metropolis dynamics on $(x, R)$ targeting
$\pi(x, R) \propto e^{-A(x)}\,P_{\mathrm{Ewens}}(R)\,e^{-U(R,x)}$ — the
annealed joint, deliberately distinct from the quenched coordinate update
$e^{-\mathbb E_w[U]}$ of amendment 10; the Jensen gap between the two is part
of the process-versus-landscape comparison and is reported, not reconciled.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

import numpy as np

from .categorical_falsification_model import (
    FalsificationModel,
    crp_partition_prior,
    kl_laws,
)
from .cocycle_flow import consecutive_blocks
from .coupling_readback import (
    PairwiseCouplings,
    PairwiseInstance,
    RescalingStep,
    _kernel_model,
    couplings_action,
    iterated_step,
    mobius_couplings,
)
from .participatory_blocking import (
    BlockingPosterior,
    blocking_posterior,
    cycle_blocking_candidates,
)
from .partition_dynamics import _evaluate_batch, _partition_tables


@dataclass(frozen=True)
class EnvironmentalDressing:
    """One pinned environmental agent per site, sharing the site's frame."""

    pinned: tuple[int, ...]
    strength: float


def _environment_field(
    model: FalsificationModel,
    dressing: EnvironmentalDressing,
) -> np.ndarray:
    r"""Return the site-by-state field $F_a(x)$ of one dressing.

    The field is the two-channel divergence of the site's state laws from the
    pinned agent's laws at identity transport, scaled by the declared strength.
    The declared families must have full support; a support failure makes the
    divergence infinite and is refused.
    """
    size = model.state_count
    if len(dressing.pinned) != len(model.agents):
        raise ValueError("a dressing must pin one environmental state per site")
    if any(
        type(value) is not int or not 0 <= value < size for value in dressing.pinned
    ):
        raise ValueError("pinned states must index the declared state space")
    strength = float(dressing.strength)
    if not math.isfinite(strength) or strength < 0.0:
        raise ValueError("the environmental strength must be finite and nonnegative")
    field = np.zeros((len(model.agents), size), dtype=np.float64)
    for position, pin in enumerate(dressing.pinned):
        pin_belief, pin_model = model.state_pair(pin)
        for state in range(size):
            belief, law = model.state_pair(state)
            value = strength * (kl_laws(belief, pin_belief) + kl_laws(law, pin_model))
            if not math.isfinite(value):
                raise ValueError(
                    "the declared families must have full support for the dressing"
                )
            field[position, state] = value
    return field


def dressed_instance(
    instance: PairwiseInstance,
    dressing: EnvironmentalDressing,
) -> PairwiseInstance:
    """Return the instance with the environmental field folded into its sites.

    The field enters anchored — zero at the declared ground state per site,
    the anchor shift absorbed into the constant — so the dressed couplings
    stay in the anchored gauge and every audited instrument applies unchanged.
    """
    model = _kernel_model(instance.graph, "environmental-dressing")
    field = _environment_field(model, dressing)
    couplings = instance.couplings
    sites = tuple(
        tuple(
            value + Fraction(float(field[position, state] - field[position, 0]))
            for state, value in enumerate(table)
        )
        for position, table in enumerate(couplings.sites)
    )
    constant = couplings.constant + sum(
        (Fraction(float(field[position, 0])) for position in range(len(couplings.sites))),
        Fraction(0),
    )
    return PairwiseInstance(
        graph=instance.graph,
        couplings=PairwiseCouplings(
            width=couplings.width,
            constant=constant,
            sites=sites,
            pairs=couplings.pairs,
        ),
    )


def environmental_parent(
    model: FalsificationModel,
    block: tuple[int, ...],
    dressing: EnvironmentalDressing,
) -> int:
    r"""Return the coarse pin of one block: the MAP parent of its pinned children.

    $\epsilon_B = \arg\min_p \sum_{a \in B} -\log K(\epsilon_a \mid p)$ under
    the declared downward kernels — the infinite-inertia (point-mass) limit of
    the audited Bayes blocking kernel.
    """
    position_of = {agent: index for index, agent in enumerate(model.agents)}
    size = model.state_count
    costs = np.zeros(size, dtype=np.float64)
    for agent in block:
        pin = dressing.pinned[position_of[agent]]
        for parent in range(size):
            kernel = model.downward_kernel(block, agent, parent)
            costs[parent] += -math.log(float(kernel[pin]))
    return int(np.argmin(costs))


def environmental_step(
    instance: PairwiseInstance,
    dressing: EnvironmentalDressing,
    blocks: tuple[tuple[int, ...], ...],
) -> tuple[RescalingStep, PairwiseInstance | None, EnvironmentalDressing]:
    """Run one audited blocking step with the environment blocked alongside.

    Dress, contract and read back through the audited route, pin the coarse
    environment at the per-block MAP parents, and undress the coarse site
    sector by the declared coarse field — exact, because the field is a site
    function. Returns the dressed step, the undressed coarse instance (None at
    a terminal single block), and the coarse dressing.
    """
    model = _kernel_model(instance.graph, "environmental-step")
    step = iterated_step(dressed_instance(instance, dressing), blocks)
    coarse_pinned = tuple(
        environmental_parent(model, tuple(block), dressing) for block in blocks
    )
    coarse_dressing = EnvironmentalDressing(
        pinned=coarse_pinned, strength=dressing.strength
    )
    if step.instance is None:
        return step, None, coarse_dressing
    coarse_model = _kernel_model(step.instance.graph, "environmental-undress")
    coarse_field = _environment_field(coarse_model, coarse_dressing)
    couplings = step.instance.couplings
    sites = tuple(
        tuple(
            value - Fraction(float(coarse_field[position, state] - coarse_field[position, 0]))
            for state, value in enumerate(table)
        )
        for position, table in enumerate(couplings.sites)
    )
    constant = couplings.constant - sum(
        (
            Fraction(float(coarse_field[position, 0]))
            for position in range(len(couplings.sites))
        ),
        Fraction(0),
    )
    undressed = PairwiseInstance(
        graph=step.instance.graph,
        couplings=PairwiseCouplings(
            width=couplings.width,
            constant=constant,
            sites=sites,
            pairs=couplings.pairs,
        ),
    )
    return step, undressed, coarse_dressing


def anchored_posterior(
    instance: PairwiseInstance,
    dressing: EnvironmentalDressing,
) -> BlockingPosterior:
    """Return the amendment-10 partition posterior of the dressed level."""
    return blocking_posterior(dressed_instance(instance, dressing))


@dataclass(frozen=True)
class SharedEnvironment:
    """Finite-inertia environmental agents, one per declared disjoint site group."""

    groups: tuple[tuple[int, ...], ...]
    preferred: tuple[int, ...]
    strength: float
    inertia: float


def _state_divergence_table(model: FalsificationModel) -> np.ndarray:
    r"""Return the strength-one two-channel divergence table $F(x, y)$."""
    size = model.state_count
    table = np.zeros((size, size), dtype=np.float64)
    for left in range(size):
        left_belief, left_model = model.state_pair(left)
        for right in range(size):
            right_belief, right_model = model.state_pair(right)
            value = kl_laws(left_belief, right_belief) + kl_laws(left_model, right_model)
            if not math.isfinite(value):
                raise ValueError(
                    "the declared families must have full support for the dressing"
                )
            table[left, right] = value
    return table


def shared_dressed_instance(
    instance: PairwiseInstance,
    environment: SharedEnvironment,
) -> PairwiseInstance:
    r"""Fold finite-inertia shared environmental agents into the couplings, exactly.

    Each group's agent carries the prior $\rho(y) \propto e^{-m F(y, \epsilon)}$
    and couples to its attached sites at strength $\kappa_{\mathrm{env}}$; it is
    integrated out exactly, and the induced group potential
    $-\log \sum_y \rho(y) e^{-\kappa \sum_a F(x_a, y)}$ is decomposed by the
    anchored Moebius route into constant, site, and (for pair groups) pair
    components — the pair component is the correlation channel a point-mass
    environment cannot carry, and it vanishes as $m \to \infty$. Groups of
    size one and two are declared; larger groups are deferred.
    """
    model = _kernel_model(instance.graph, "shared-environment")
    size = model.state_count
    length = len(model.agents)
    seen: set[int] = set()
    for group in environment.groups:
        for site in group:
            if type(site) is not int or not 1 <= site <= length or site in seen:
                raise ValueError("groups must be disjoint sets of declared sites")
            seen.add(site)
        if len(group) not in (1, 2):
            raise ValueError("declared group sizes are one and two")
    if len(environment.preferred) != len(environment.groups):
        raise ValueError("one preferred state per group is required")
    if any(
        type(value) is not int or not 0 <= value < size
        for value in environment.preferred
    ):
        raise ValueError("preferred states must index the declared state space")
    strength = float(environment.strength)
    inertia = float(environment.inertia)
    if not math.isfinite(strength) or strength < 0.0:
        raise ValueError("the environmental strength must be finite and nonnegative")
    if not math.isfinite(inertia) or inertia < 0.0:
        raise ValueError("the environmental inertia must be finite and nonnegative")
    divergence = _state_divergence_table(model)
    couplings = instance.couplings
    site_tables = [list(table) for table in couplings.sites]
    pair_tables: dict[tuple[int, int], list[list[Fraction]]] = {
        pair: [list(row) for row in table] for pair, table in couplings.pairs
    }
    constant = couplings.constant
    for group, preferred in zip(environment.groups, environment.preferred):
        log_prior = -inertia * divergence[:, preferred]
        log_prior = log_prior - float(np.max(log_prior))
        prior = np.exp(log_prior)
        prior = prior / prior.sum()
        if len(group) == 1:
            position = group[0] - 1
            induced = -np.log(
                np.einsum("y,xy->x", prior, np.exp(-strength * divergence))
            )
            for state in range(size):
                site_tables[position][state] += Fraction(
                    float(induced[state] - induced[0])
                )
            constant += Fraction(float(induced[0]))
            continue
        left, right = sorted(position - 1 for position in group)
        boltzmann = np.exp(-strength * divergence)
        induced = -np.log(
            np.einsum("xy,zy,y->xz", boltzmann, boltzmann, prior)
        )
        action = {
            (row, column): Fraction(float(induced[row, column]))
            for row in range(size)
            for column in range(size)
        }
        decomposed, omitted = mobius_couplings(action, ((0, 1),))
        if omitted != Fraction(0):
            raise ValueError("a width-two decomposition cannot omit anything")
        for state in range(size):
            site_tables[left][state] += decomposed.sites[0][state]
            site_tables[right][state] += decomposed.sites[1][state]
        pair_table = dict(decomposed.pairs)[(0, 1)]
        existing = pair_tables.setdefault(
            (left, right), [[Fraction(0)] * size for _ in range(size)]
        )
        for row in range(size):
            for column in range(size):
                existing[row][column] += pair_table[row][column]
        constant += decomposed.constant
    return PairwiseInstance(
        graph=instance.graph,
        couplings=PairwiseCouplings(
            width=couplings.width,
            constant=constant,
            sites=tuple(tuple(table) for table in site_tables),
            pairs=tuple(
                sorted(
                    (pair, tuple(tuple(row) for row in table))
                    for pair, table in pair_tables.items()
                )
            ),
        ),
    )


def induced_pair_sup(
    instance: PairwiseInstance,
    environment: SharedEnvironment,
) -> float:
    """Return the sup of the environment-induced pair components alone."""
    bare_pairs = {
        pair: table for pair, table in instance.couplings.pairs
    }
    dressed = shared_dressed_instance(instance, environment)
    supremum = 0.0
    for pair, table in dressed.couplings.pairs:
        bare = bare_pairs.get(pair)
        for row_index, row in enumerate(table):
            for column_index, value in enumerate(row):
                base = bare[row_index][column_index] if bare is not None else Fraction(0)
                supremum = max(supremum, abs(float(value - base)))
    return supremum


@dataclass(frozen=True)
class DescentReport:
    """M-flow: dynamical class occupancies of the joint (state, partition) walk."""

    steps: int
    burn_in: int
    replicas: int
    class_occupancies: tuple[tuple[int, float], ...]
    per_replica_modal: tuple[int, ...]
    acceptance_rate: float


def coupled_blocking_descent(
    instance: PairwiseInstance,
    dressing: EnvironmentalDressing | None = None,
    steps: int = 20000,
    burn_in: int = 5000,
    seeds: tuple[int, ...] = (0, 1, 2),
) -> DescentReport:
    r"""Run the joint Metropolis walk on $(x, R)$ and report class occupancies.

    The target is $\pi(x, R) \propto e^{-A(x)}\,P_{\mathrm{Ewens}}(R)\,
    e^{-U(R,x)}$ with $A$ the (dressed) coupling action and $U$ the derived
    M5 energy — the annealed joint, distinct from amendment 10's quenched
    coordinate update, with the gap between them part of what is measured.
    Moves alternate at probability one half between a uniform single-site
    state proposal and a uniform candidate partition proposal.
    """
    working = (
        instance if dressing is None else dressed_instance(instance, dressing)
    )
    model = _kernel_model(working.graph, "coupled-blocking-descent")
    size = model.state_count
    length = len(working.graph.vertices)
    action = np.asarray(couplings_action(working.couplings), dtype=np.float64)
    declared = cycle_blocking_candidates(length)
    tables = [_partition_tables(model, partition) for _, partition in declared]
    log_prior = np.array(
        [
            math.log(float(crp_partition_prior(partition, model.crp_concentration)))
            for _, partition in declared
        ]
    )

    def block_energy_at(candidate: int, states: np.ndarray) -> float:
        cross, graph, _ = _evaluate_batch(tables[candidate], states[None, :])
        return float(cross[0]) + float(graph[0])

    occupancy = np.zeros(len(declared), dtype=np.float64)
    per_replica_modal: list[int] = []
    accepted = 0
    proposed = 0
    for seed in seeds:
        rng = np.random.default_rng(seed)
        states = rng.integers(0, size, size=length, dtype=np.int64)
        candidate = 0
        energy_u = block_energy_at(candidate, states)
        replica_occupancy = np.zeros(len(declared), dtype=np.float64)
        for step_index in range(steps):
            proposed += 1
            if rng.random() < 0.5:
                site = int(rng.integers(0, length))
                value = int(rng.integers(0, size))
                trial = states.copy()
                trial[site] = value
                trial_u = block_energy_at(candidate, trial)
                delta = (
                    float(action[tuple(trial)])
                    - float(action[tuple(states)])
                    + trial_u
                    - energy_u
                )
                if delta <= 0.0 or rng.random() < math.exp(-delta):
                    states = trial
                    energy_u = trial_u
                    accepted += 1
            else:
                trial_candidate = int(rng.integers(0, len(declared)))
                trial_u = block_energy_at(trial_candidate, states)
                delta = (trial_u - energy_u) - (
                    log_prior[trial_candidate] - log_prior[candidate]
                )
                if delta <= 0.0 or rng.random() < math.exp(-delta):
                    candidate = trial_candidate
                    energy_u = trial_u
                    accepted += 1
            if step_index >= burn_in:
                replica_occupancy[candidate] += 1.0
        replica_occupancy /= replica_occupancy.sum()
        occupancy += replica_occupancy
        ratios = np.array([ratio for ratio, _ in declared])
        replica_classes: dict[int, float] = {}
        for ratio, mass in zip(ratios, replica_occupancy):
            replica_classes[int(ratio)] = replica_classes.get(int(ratio), 0.0) + float(mass)
        per_replica_modal.append(max(replica_classes, key=replica_classes.get))
    occupancy /= len(seeds)
    classes: dict[int, float] = {}
    for (ratio, _), mass in zip(declared, occupancy):
        classes[ratio] = classes.get(ratio, 0.0) + float(mass)
    return DescentReport(
        steps=steps,
        burn_in=burn_in,
        replicas=len(seeds),
        class_occupancies=tuple(sorted(classes.items())),
        per_replica_modal=tuple(per_replica_modal),
        acceptance_rate=accepted / proposed if proposed else 0.0,
    )


__all__ = [
    "DescentReport",
    "EnvironmentalDressing",
    "SharedEnvironment",
    "anchored_posterior",
    "coupled_blocking_descent",
    "dressed_instance",
    "environmental_parent",
    "environmental_step",
    "induced_pair_sup",
    "shared_dressed_instance",
]
