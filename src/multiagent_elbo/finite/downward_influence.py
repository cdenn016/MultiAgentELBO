"""Measurement M6, downward influence of the parent on its children.

Intervening on the parent means replacing the block's parent state by a declared
value and recomputing the child's exact recognition optimum,

    Q(child | parent) proportional to K_down(child | parent) exp(-E),

where E is the child's scale-zero energy, here the negative log of the declared
per-agent evaluator-averaged likelihood at one record entry. The reported quantity
is the supremum over ordered pairs of parent values of the total variation distance
between the two optima. It is zero exactly when the parent cannot move the child at
all, which is the pre-registered falsifier: a meta-agent that cannot move its
children is decorative.

The control replaces the declared kernel by the fiber disintegration of a
deterministic pushforward parent. If the parent is a deterministic statistic C of
its children then the joint is the child law times a point mass, so the top-down
kernel is forced to be the disintegration of the child law over the fibers of C and
the parent prior is forced to be the pushforward of the child law. Nothing about
the top-down kernel remains free, and the parent supplies no conditional randomness
beyond what is already a function of the children. The declared statistic here
carries each member law into the block root frame by the spanning-tree transport
and takes the coordinatewise modal presentation in each channel, ties broken by the
smallest family index, which is exactly a deterministic many-to-one statistic of
the children. The same supremum then measures only the variation between fibers of
C, since inside a fiber the child law is the reference law renormalized and the
parent value is constant.

The disintegration needs a declared reference child law, and the number depends on
which one is declared, so both are computed rather than one being chosen after the
fact. The exchangeable reference is the product of uniform member laws, which is the
maximum-entropy child law of a model whose parent is a function of its children and
therefore cannot correlate them; it is the default. The generative reference is the
child marginal of the declared generative model under a uniform parent prior, which
keeps the child law of the original model and changes only the arrow. Under the
generative reference the deterministic statistic is a nearly sufficient readout of
the latent parent on a large block, so its fiber disintegration approaches the
declared kernel from above rather than collapsing.

Both numbers are reported per block and per agent. Nothing here is tuned: the
kernel, the energy, the statistic and both reference child laws are declared before
the numbers are read.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Optional, Sequence

import numpy as np

from .categorical_falsification_model import FalsificationModel, Partition
from .two_channel_gauge import Law

DEFAULT_OUTCOME = 1
DEFAULT_REFERENCE = "exchangeable"
REFERENCE_CHILD_LAWS = ("exchangeable", "generative")


@dataclass(frozen=True)
class InfluenceReport:
    """Hold the declared and controlled downward influence of one parent on one child."""

    model_name: str
    block: tuple[int, ...]
    agent: int
    outcome: int
    influence: float
    control: float
    generative_reference_control: float
    collapse_ratio: float
    influence_falsifier_fired: bool
    control_collapsed: bool


def total_variation(left: np.ndarray, right: np.ndarray) -> float:
    """Return the total variation distance of two laws on the same finite set."""
    if left.shape != right.shape:
        raise ValueError("laws must share a shape")
    return 0.5 * float(np.abs(left - right).sum())


def _family(model: FalsificationModel, channel: str) -> tuple[Law, ...]:
    """Return the admitted presentation family of one channel."""
    if channel == "belief":
        return model.belief_family
    if channel == "model":
        return model.model_family
    raise ValueError("channel must be 'belief' or 'model'")


def _action_table(model: FalsificationModel, channel: str) -> np.ndarray:
    """Return table[k, a], the family index of the k-transport of family member a."""
    family = _family(model, channel)
    representation = (
        model.belief_representation if channel == "belief" else model.model_representation
    )
    index_of = {law: index for index, law in enumerate(family)}
    table = np.zeros((model.graph.order, len(family)), dtype=np.int64)
    for element in range(model.graph.order):
        for index, law in enumerate(family):
            table[element, index] = index_of[representation.act(element, law)]
    return table


def coarse_statistic(
    model: FalsificationModel,
    block: Sequence[int],
    states: Sequence[int],
) -> int:
    """Return the declared deterministic parent statistic of one block configuration.

    Each member presentation is carried into the block root frame by the spanning
    tree transport and the parent coordinate of a channel is the modal transported
    family index over the members, ties broken by the smallest index. On a block
    whose members are exactly consistent with some parent state the statistic
    returns that state, so the deterministic parent is a genuine coarse graining
    rather than a relabeling of one distinguished child.
    """
    members = tuple(block)
    if len(states) != len(members):
        raise ValueError("states must carry one index per block member")
    model_size = len(model.model_family)
    coordinates: list[int] = []
    for channel in ("belief", "model"):
        family_size = len(_family(model, channel))
        action = _action_table(model, channel)
        transports = model.block_transports(members, channel)
        counts = np.zeros(family_size, dtype=np.int64)
        for member, state in zip(members, states):
            index = state // model_size if channel == "belief" else state % model_size
            counts[action[transports[member], index]] += 1
        coordinates.append(int(np.argmax(counts)))
    return coordinates[0] * model_size + coordinates[1]


def child_optimum(
    model: FalsificationModel,
    block: Sequence[int],
    agent: int,
    parent_state: int,
    outcome: int = DEFAULT_OUTCOME,
) -> np.ndarray:
    """Return the child's exact recognition optimum under one intervened parent state.

    The optimum is the declared downward kernel reweighted by the exponential of the
    negative scale-zero energy, which for this instance is the per-agent evaluator
    averaged likelihood at the declared record entry. Both factors are strictly
    positive on the finite presentation space, so the optimum is a strictly positive
    law and the normalizer is finite.
    """
    if type(outcome) is not int or outcome not in (0, 1):
        raise ValueError("outcome must be 0 or 1")
    kernel = model.downward_kernel(block, agent, parent_state)
    weights = kernel * model.likelihood_table()[:, outcome]
    return weights / weights.sum()


def downward_influence(
    model: FalsificationModel,
    block: Sequence[int],
    agent: int,
    outcome: int = DEFAULT_OUTCOME,
) -> float:
    """Return the supremum total variation between child optima over parent states."""
    optima = [
        child_optimum(model, block, agent, parent, outcome)
        for parent in range(model.state_count)
    ]
    return max(
        total_variation(optima[left], optima[right])
        for left in range(len(optima))
        for right in range(len(optima))
    )


def _channel_marginals(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
    reference: str,
) -> np.ndarray:
    """Return marginal[mixture component, member, family index] of the reference child law."""
    members = tuple(block)
    model_size = len(model.model_family)
    family_size = len(_family(model, channel))
    if reference == "exchangeable":
        return np.full((1, len(members), family_size), 1.0 / family_size, dtype=np.float64)
    if reference != "generative":
        raise ValueError("reference must be 'exchangeable' or 'generative'")
    marginals = np.zeros((model.state_count, len(members), family_size), dtype=np.float64)
    for position, member in enumerate(members):
        for parent in range(model.state_count):
            kernel = model.downward_kernel(members, member, parent)
            grid = kernel.reshape(len(model.belief_family), model_size)
            marginals[parent, position] = grid.sum(axis=1) if channel == "belief" else grid.sum(axis=0)
    return marginals


def _channel_fiber_joint(
    model: FalsificationModel,
    block: Sequence[int],
    agent: int,
    channel: str,
    reference: str,
) -> np.ndarray:
    """Return joint[mixture component, child index, statistic index] within one channel."""
    members = tuple(block)
    position = members.index(agent)
    family_size = len(_family(model, channel))
    action = _action_table(model, channel)
    transports = model.block_transports(members, channel)
    carried = np.array(
        [[action[transports[member], index] for index in range(family_size)] for member in members],
        dtype=np.int64,
    )
    marginals = _channel_marginals(model, block, channel, reference)
    components = marginals.shape[0]
    joint = np.zeros((components, family_size, family_size), dtype=np.float64)
    for component in range(components):
        for configuration in product(range(family_size), repeat=len(members)):
            mass = 1.0
            counts = np.zeros(family_size, dtype=np.int64)
            for member_position, index in enumerate(configuration):
                mass *= marginals[component, member_position, index]
                counts[carried[member_position, index]] += 1
            joint[component, configuration[position], int(np.argmax(counts))] += mass
    return joint


def fiber_disintegration(
    model: FalsificationModel,
    block: Sequence[int],
    agent: int,
    reference: str = DEFAULT_REFERENCE,
) -> np.ndarray:
    """Return the forced top-down kernel of a deterministic pushforward parent.

    Column c of the returned array is the conditional law of the child given that the
    declared deterministic statistic equals c, which is the fiber disintegration that
    Proposition 3(a) forces once the parent is a function of its children. The
    exchangeable reference child law is the product of uniform member laws and the
    generative reference child law is the marginal of the declared generative model
    under a uniform parent prior. Statistic values outside the range of the statistic
    carry no mass and their columns are returned as zeros, because intervening there
    is a null operation rather than an intervention.
    """
    belief_joint = _channel_fiber_joint(model, block, agent, "belief", reference)
    model_joint = _channel_fiber_joint(model, block, agent, "model", reference)
    states = model.state_count
    components = belief_joint.shape[0]
    joint = np.zeros((states, states), dtype=np.float64)
    for component in range(components):
        block_joint = np.einsum(
            "ab,cd->acbd", belief_joint[component], model_joint[component]
        ).reshape(states, states)
        joint += block_joint / components
    columns = joint.sum(axis=0)
    kernel = np.zeros_like(joint)
    live = columns > 0.0
    kernel[:, live] = joint[:, live] / columns[live]
    return kernel


def deterministic_control(
    model: FalsificationModel,
    block: Sequence[int],
    agent: int,
    outcome: int = DEFAULT_OUTCOME,
    reference: str = DEFAULT_REFERENCE,
) -> float:
    """Return the same supremum after forcing the deterministic pushforward parent.

    The supremum runs over the range of the statistic only, since Proposition 3(b)
    makes intervention outside that range a null operation. Inside the range the
    child law is the reference law restricted to the fiber and renormalized, so the
    number measures between-fiber variation and nothing else.
    """
    if type(outcome) is not int or outcome not in (0, 1):
        raise ValueError("outcome must be 0 or 1")
    kernel = fiber_disintegration(model, block, agent, reference)
    likelihood = model.likelihood_table()[:, outcome]
    optima: list[np.ndarray] = []
    for statistic in range(model.state_count):
        column = kernel[:, statistic]
        if column.sum() == 0.0:
            continue
        weights = column * likelihood
        optima.append(weights / weights.sum())
    return max(
        total_variation(optima[left], optima[right])
        for left in range(len(optima))
        for right in range(len(optima))
    )


def influence_report(
    model: FalsificationModel,
    partition: Optional[Partition] = None,
    outcome: int = DEFAULT_OUTCOME,
) -> tuple[InfluenceReport, ...]:
    """Report the declared influence and the deterministic control per block and agent."""
    blocks = partition if partition is not None else model.candidate_partitions[0]
    reports: list[InfluenceReport] = []
    for block in blocks:
        for agent in block:
            influence = downward_influence(model, block, agent, outcome)
            control = deterministic_control(model, block, agent, outcome, "exchangeable")
            generative = deterministic_control(model, block, agent, outcome, "generative")
            reports.append(
                InfluenceReport(
                    model_name=model.name,
                    block=tuple(block),
                    agent=int(agent),
                    outcome=outcome,
                    influence=influence,
                    control=control,
                    generative_reference_control=generative,
                    collapse_ratio=control / influence if influence > 0.0 else float("nan"),
                    influence_falsifier_fired=influence == 0.0,
                    control_collapsed=control < influence,
                )
            )
    return tuple(reports)


__all__ = [
    "DEFAULT_OUTCOME",
    "DEFAULT_REFERENCE",
    "InfluenceReport",
    "REFERENCE_CHILD_LAWS",
    "child_optimum",
    "coarse_statistic",
    "deterministic_control",
    "downward_influence",
    "fiber_disintegration",
    "influence_report",
    "total_variation",
]
