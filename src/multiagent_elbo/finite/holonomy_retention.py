"""Holonomy retention scores, dressed transport laws, and the logical-chain witnesses.

This is measurement four of the finite categorical falsification design. Per
candidate block, per channel, and per declared admitted parent family it computes
the based holonomy group of the induced subgraph, the fixed sector that group
leaves invariant inside the admitted family, and the retention score, the infimum
over the fixed sector of the occupancy-weighted forward divergence from the
root-framed member laws. The infimum over an empty fixed sector is positive
infinity, which is the exact way a block with nontrivial holonomy reports that no
admitted parent presentation can be simultaneously parallel to its children.

The second half of the module works at the coarse tier. It builds the full
conditional law of dressed microscopic transports rather than a mean, carries the
endpoint kernel inside the numerator over every ordered pair, and keeps the wrong
restricted numerator beside it as a negative control. The stabilizer criterion is
stated as a mass, the barycenter is computed but never composed or inverted, and
only the forward direction of the composition proposition is asserted.

Conventions inherited from the gauge module: an ordered pair is
``(receiver, source)``, a tree transport carries a member frame into the block root
frame, and the abelian structure group turns every walk transport into a signed sum
of edge elements. Exact rational arithmetic is used wherever a quantity is a
finite sum of declared rationals; floating point enters only through logarithms and
through the float-valued edge event law of the declared model.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import math
from typing import Mapping, Sequence

import numpy as np

from .categorical_falsification_model import (
    GROUP_ORDER,
    FalsificationModel,
    Partition,
    kl_laws,
    transported,
)
from .two_channel_gauge import (
    CyclicRepresentation,
    Law,
    TwoChannelGraph,
    based_holonomy_generators,
    fixed_laws,
    fixed_simplex_laws,
    generated_subgroup,
    tree_transport_elements,
    uniform_law,
)

CHANNELS = ("belief", "model")
ADMITTED_FAMILIES = ("orbit", "simplex")
REFERENCE_STATE_INDICES = (0, 4, 8, 1, 5, 6)


def _check_channel(channel: str) -> None:
    """Raise unless the channel is one of the two declared channels."""
    if type(channel) is not str or channel not in CHANNELS:
        raise ValueError("channel must be 'belief' or 'model'")


def _check_admitted(admitted: str) -> None:
    """Raise unless the admitted parent family is one of the two declared families."""
    if type(admitted) is not str or admitted not in ADMITTED_FAMILIES:
        raise ValueError("admitted must be 'orbit' or 'simplex'")


def _representation(model: FalsificationModel, channel: str) -> CyclicRepresentation:
    """Return the representation of one declared channel."""
    _check_channel(channel)
    if channel == "belief":
        return model.belief_representation
    return model.model_representation


def _family(model: FalsificationModel, channel: str) -> tuple[Law, ...]:
    """Return the declared finite presentation family of one channel."""
    _check_channel(channel)
    if channel == "belief":
        return model.belief_family
    return model.model_family


def _channel_law(model: FalsificationModel, channel: str, state: int) -> Law:
    """Return the law of one channel inside one joint agent state."""
    _check_channel(channel)
    belief, model_law = model.state_pair(state)
    return belief if channel == "belief" else model_law


def _state_index(model: FalsificationModel, channel: str, law: Law) -> int:
    """Return a joint state index whose named channel carries the requested law."""
    family = _family(model, channel)
    if law not in family:
        raise ValueError("the requested law is not a declared presentation")
    position = family.index(law)
    if channel == "belief":
        return position * len(model.model_family)
    return position


def _components(graph: TwoChannelGraph) -> tuple[tuple[int, ...], ...]:
    """Return the weakly connected components of a graph, sorted inside and out."""
    parent = {vertex: vertex for vertex in graph.vertices}

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in graph.edges:
        left, right = find(edge.receiver), find(edge.source)
        if left != right:
            parent[left] = right
    groups: dict[int, list[int]] = {}
    for vertex in graph.vertices:
        groups.setdefault(find(vertex), []).append(vertex)
    return tuple(sorted(tuple(sorted(members)) for members in groups.values()))


def block_components(model: FalsificationModel, block: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    """Return the connected components of the subgraph induced on a block."""
    return _components(model.graph.induced(block))


def block_holonomy_group(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
) -> tuple[int, ...]:
    """Return the based holonomy group of a block, pooled over its components.

    Each component is rooted at its own smallest member and contributes the based
    generators of its own cycle basis. A disconnected block has no single root, so
    pooling the component generators is the honest reading of `the group of loop
    transports available inside this block`, and it agrees with the single-root
    construction whenever the block is connected.
    """
    _check_channel(channel)
    induced = model.graph.induced(block)
    generators: list[int] = []
    for component in _components(induced):
        component_graph = induced.induced(component)
        generators.extend(
            based_holonomy_generators(component_graph, channel, min(component))
        )
    return generated_subgroup(model.graph.order, tuple(generators))


def block_transport_elements(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
) -> dict[int, int]:
    """Return the group element carrying each member frame to its component root.

    On a connected block this is exactly the declared block transport of the model,
    rooted at the smallest member. On a disconnected block each component is rooted
    separately, and the relative alignment of distinct component roots is left free
    rather than silently fixed at the identity.
    """
    _check_channel(channel)
    induced = model.graph.induced(block)
    transports: dict[int, int] = {}
    for component in _components(induced):
        component_graph = induced.induced(component)
        transports.update(
            tree_transport_elements(component_graph, channel, min(component))
        )
    return transports


def _block_weights(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
) -> dict[int, Fraction]:
    """Return the occupancy weights of a block, normalized to sum to exactly one."""
    _check_channel(channel)
    occupancy = model.alpha_belief if channel == "belief" else model.alpha_model
    position_of = {agent: index for index, agent in enumerate(model.agents)}
    masses: dict[int, Fraction] = {}
    for agent in block:
        if agent not in position_of:
            raise ValueError("a block member is not a declared agent")
        masses[agent] = occupancy[position_of[agent]]
    total = sum(masses.values(), Fraction(0))
    if total == 0:
        raise ValueError("a block must carry positive occupancy")
    return {agent: mass / total for agent, mass in masses.items()}


def fixed_sector(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
    admitted: str,
) -> tuple[Law, ...]:
    """Return the sector of admitted parent laws fixed by the whole block holonomy.

    Under the orbit family the returned tuple is the fixed sector itself, a subset
    of the declared finite presentation family. Under the simplex family the fixed
    sector is a convex set and the returned tuple lists its extreme points, the
    normalized indicators of the orbits of the induced permutation group; the
    sector is their convex hull and it is a single point exactly when that group is
    transitive. The stabilizer of a nontrivial cyclic shift on the simplex is the
    uniform law alone, so a block with nontrivial holonomy has an empty orbit-family
    sector and a one-point simplex sector.
    """
    _check_admitted(admitted)
    representation = _representation(model, channel)
    elements = block_holonomy_group(model, block, channel)
    if admitted == "orbit":
        return fixed_laws(representation, elements, _family(model, channel))
    return fixed_simplex_laws(representation, elements)


def _alignments(order: int, components: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    """Return the admissible relative alignments of the component roots of a block."""
    if len(components) == 1:
        return ((0,),)
    return tuple(product(range(order), repeat=len(components)))


def transported_laws(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
    states: Mapping[int, int],
    alignment: Sequence[int],
) -> dict[int, Law]:
    """Return the root-framed law of every block member under one root alignment."""
    representation = _representation(model, channel)
    order = model.graph.order
    transports = block_transport_elements(model, block, channel)
    components = block_components(model, block)
    if len(alignment) != len(components):
        raise ValueError("an alignment must carry one element per component")
    carried: dict[int, Law] = {}
    for component, shift in zip(components, alignment):
        for agent in component:
            if agent not in states:
                raise ValueError("every block member needs a declared state")
            element = (transports[agent] + shift) % order
            carried[agent] = transported(
                representation, element, _channel_law(model, channel, states[agent])
            )
    return carried


def _mixture(carried: Mapping[int, Law], weights: Mapping[int, Fraction]) -> Law:
    """Return the exact occupancy-weighted mixture of the root-framed laws."""
    order = len(next(iter(carried.values())))
    blended = [Fraction(0) for _ in range(order)]
    for agent, law in carried.items():
        weight = weights[agent]
        for index in range(order):
            blended[index] += weight * law[index]
    return tuple(blended)


def _simplex_projection(extreme_points: Sequence[Law], mixture: Law) -> Law:
    """Return the fixed-sector law minimizing the weighted forward divergence.

    The extreme points have disjoint supports, so a law in their hull is constant
    on each support. Minimizing the weighted forward divergence therefore reduces
    to maximizing a sum of the form total mass times the logarithm of a hull
    coefficient, whose optimum places on each extreme point the mixture mass of its
    support. The result is the mixture averaged inside each support, and it is the
    mixture itself when every support is a single point.
    """
    order = len(mixture)
    projected = [Fraction(0) for _ in range(order)]
    for indicator in extreme_points:
        support = tuple(index for index in range(order) if indicator[index] > 0)
        mass = sum((mixture[index] for index in support), Fraction(0))
        for index in support:
            projected[index] = mass * indicator[index]
    return tuple(projected)


def _weighted_forward_kl(
    carried: Mapping[int, Law],
    weights: Mapping[int, Fraction],
    target: Law,
) -> float:
    """Return the occupancy-weighted forward divergence of root-framed laws to a target."""
    total = 0.0
    for agent, law in carried.items():
        divergence = float(kl_laws(law, target))
        if math.isinf(divergence):
            return math.inf
        total += float(weights[agent]) * divergence
    return float(total)


def holonomy_distortion(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
    admitted: str,
    states: Mapping[int, int],
) -> float:
    """Return the retention score of a block, infinite when the fixed sector is empty.

    The score is the infimum over the fixed sector of the occupancy-weighted forward
    divergence from each root-framed member law to the candidate parent, with the
    convention that an infimum over the empty set is positive infinity. The orbit
    family is searched by exact enumeration; the simplex family is minimized in
    closed form, since the forward-divergence minimizer inside the hull of
    disjointly supported indicators is the weighted mixture averaged within each
    support. On a disconnected block the infimum also runs over the relative
    alignments of the component roots, which is the best case of the declared
    channel that collapses distinct component roots onto one parent root.
    """
    _check_admitted(admitted)
    sector = fixed_sector(model, block, channel, admitted)
    if not sector:
        return math.inf
    weights = _block_weights(model, block, channel)
    components = block_components(model, block)
    best = math.inf
    for alignment in _alignments(model.graph.order, components):
        carried = transported_laws(model, block, channel, states, alignment)
        if admitted == "orbit":
            value = min(_weighted_forward_kl(carried, weights, target) for target in sector)
        else:
            target = _simplex_projection(sector, _mixture(carried, weights))
            value = _weighted_forward_kl(carried, weights, target)
        best = min(best, value)
    return float(best)


def _law_in_sector(sector: Sequence[Law], admitted: str, law: Law) -> bool:
    """Report whether one law lies in the fixed sector under the admitted family."""
    if admitted == "orbit":
        return law in tuple(sector)
    return _simplex_projection(sector, law) == law


def zero_distortion_is_attainable(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
    admitted: str,
) -> bool:
    """Report whether some state configuration of a block drives its score to zero.

    The score vanishes exactly when every root-framed law coincides with one law of
    the fixed sector. Because the presentation family is a single orbit and is
    closed under the representation, any fixed-sector member that is itself a
    declared presentation is reachable by pulling it back along the tree transports,
    and no other target can be reached. The test is therefore a membership question
    rather than a search over configurations.
    """
    _check_admitted(admitted)
    sector = fixed_sector(model, block, channel, admitted)
    if not sector:
        return False
    return any(_law_in_sector(sector, admitted, law) for law in _family(model, channel))


def aligned_state_configuration(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
    target: Law,
) -> dict[int, int]:
    """Return the block states whose root-framed laws all equal one target law.

    Each member is given the pullback of the target along its own tree transport,
    which is a declared presentation because the family is closed under the
    representation. The other channel of every joint state is left at its first
    declared presentation, since the score of one channel does not read the other.
    """
    representation = _representation(model, channel)
    order = model.graph.order
    transports = block_transport_elements(model, block, channel)
    configuration: dict[int, int] = {}
    for agent in block:
        pullback = transported(representation, (-transports[agent]) % order, target)
        configuration[agent] = _state_index(model, channel, pullback)
    return configuration


def reference_states(model: FalsificationModel) -> dict[int, int]:
    """Return the declared per-agent state configuration used for the reported scores."""
    if len(model.agents) > len(REFERENCE_STATE_INDICES):
        raise ValueError("the declared state configuration is shorter than the agent list")
    return {
        agent: REFERENCE_STATE_INDICES[position] % model.state_count
        for position, agent in enumerate(model.agents)
    }


@dataclass(frozen=True)
class EndpointKernel:
    """A soft endpoint kernel over ordered coarse pairs given ordered agent pairs.

    The kernel is the product of the two declared endpoint memberships,
    one for the receiver and one for the source, so it is normalized over ordered
    coarse pairs for every ordered agent pair. Softness is the point: an agent may
    carry positive membership in more than one coarse label, in which case the
    predicate `the agent belongs to this label` is not defined and the restricted
    dressed numerator stops being a probability measure.
    """

    labels: tuple[str, ...]
    agents: tuple[int, ...]
    weights: tuple[tuple[Fraction, ...], ...]

    def __post_init__(self) -> None:
        if type(self.labels) is not tuple or not self.labels:
            raise ValueError("labels must be a nonempty tuple")
        if type(self.agents) is not tuple or not self.agents:
            raise ValueError("agents must be a nonempty tuple")
        if len(set(self.labels)) != len(self.labels):
            raise ValueError("labels must be distinct")
        if len(set(self.agents)) != len(self.agents):
            raise ValueError("agents must be distinct")
        if len(self.weights) != len(self.agents):
            raise ValueError("weights must carry one row per agent")
        for row in self.weights:
            if len(row) != len(self.labels):
                raise ValueError("weight rows must carry one entry per label")
            for entry in row:
                if type(entry) is not Fraction:
                    raise TypeError("membership entries must be exact rationals")
                if entry < 0:
                    raise ValueError("membership entries must be nonnegative")
            if sum(row, Fraction(0)) != 1:
                raise ValueError("membership rows must sum to exactly one")

    def membership(self, label: str, agent: int) -> Fraction:
        """Return the declared membership of one agent in one coarse label."""
        if label not in self.labels:
            raise ValueError("unknown coarse label")
        if agent not in self.agents:
            raise ValueError("unknown agent")
        return self.weights[self.agents.index(agent)][self.labels.index(label)]

    def mass(self, coarse_pair: tuple[str, str], pair: tuple[int, int]) -> Fraction:
        """Return the endpoint kernel mass of one ordered coarse pair given one edge."""
        left, right = coarse_pair
        receiver, source = pair
        return self.membership(left, receiver) * self.membership(right, source)

    def block(self, label: str) -> tuple[int, ...]:
        """Return the agents carrying positive membership in one coarse label."""
        return tuple(agent for agent in self.agents if self.membership(label, agent) > 0)


def declared_endpoint_kernel(model: FalsificationModel) -> EndpointKernel:
    """Return the declared soft endpoint kernel of the six-agent reference instance.

    Two agents split their membership evenly across neighboring coarse labels, which
    is the smallest configuration that makes the restricted dressed numerator fail
    to normalize. Every coarse label induces a connected block, so the dressed
    transports are computed at a single root per label.
    """
    if len(model.agents) != 6 or len(model.parent_labels) != 3:
        raise ValueError("the declared endpoint kernel is stated for the reference instance")
    half = Fraction(1, 2)
    one = Fraction(1)
    zero = Fraction(0)
    return EndpointKernel(
        labels=tuple(model.parent_labels),
        agents=tuple(model.agents),
        weights=(
            (one, zero, zero),
            (one, zero, zero),
            (half, half, zero),
            (zero, one, zero),
            (zero, one, zero),
            (zero, half, half),
        ),
    )


def _edge_elements(model: FalsificationModel, channel: str) -> dict[tuple[int, int], int]:
    """Return the per-pair group element, with undeclared self loops carrying identity."""
    _check_channel(channel)
    elements = model.graph.channel_elements(channel)
    table: dict[tuple[int, int], int] = {(agent, agent): 0 for agent in model.agents}
    for edge, element in zip(model.graph.edges, elements):
        table[(edge.receiver, edge.source)] = element
    return table


def _dressed_numerators(
    model: FalsificationModel,
    channel: str,
    endpoint_kernel: EndpointKernel,
    coarse_pair: tuple[str, str],
    configuration: str,
) -> tuple[dict[int, Fraction], Fraction, Fraction]:
    """Return the exact dressed numerators, their total, and the restricted total.

    The dressed transport of an ordered microscopic pair is the composite
    ``tau(I from i)`` then the edge element ``g(i from j)`` then ``tau(J from j)``
    inverted. The last leg is inverted because the stored tree transport carries the
    source frame up to its own block root, while the dressed transport needs the
    opposite leg, from the coarse node J down to the microscopic source j. In the
    abelian structure group this is the signed sum
    ``tau_left[i] + g[i, j] - tau_right[j]`` reduced modulo the group order.

    The denominator and the correct numerator both run over every ordered pair and
    both carry the endpoint kernel. The restricted total instead sums the edge event
    law over the pairs whose endpoints have positive membership, dropping the kernel
    factor, and is retained only as the negative control.
    """
    _check_channel(channel)
    order = model.graph.order
    event_law = model.edge_event_law(configuration, channel)
    elements = _edge_elements(model, channel)
    left, right = coarse_pair
    left_block = endpoint_kernel.block(left)
    right_block = endpoint_kernel.block(right)
    transports_left = block_transport_elements(model, left_block, channel)
    transports_right = block_transport_elements(model, right_block, channel)
    numerators = {element: Fraction(0) for element in range(order)}
    total = Fraction(0)
    restricted = Fraction(0)
    for receiver_index, receiver in enumerate(model.agents):
        for source_index, source in enumerate(model.agents):
            event = Fraction(float(event_law[receiver_index, source_index]))
            if event == 0:
                continue
            if (receiver, source) not in elements:
                raise ValueError("the edge event law charges an undeclared ordered pair")
            if receiver in left_block and source in right_block:
                restricted += event
            weight = event * endpoint_kernel.mass(coarse_pair, (receiver, source))
            if weight == 0:
                continue
            dressed = (
                transports_left[receiver]
                + elements[(receiver, source)]
                - transports_right[source]
            ) % order
            numerators[dressed] += weight
            total += weight
    if total == 0:
        raise ValueError("the coarse pair carries no edge mass")
    return numerators, total, restricted


def exact_dressed_transport_law(
    model: FalsificationModel,
    channel: str,
    endpoint_kernel: EndpointKernel,
    coarse_pair: tuple[str, str],
    configuration: str = "uniform",
) -> dict[int, Fraction]:
    """Return the exact conditional law of dressed transports on one coarse pair."""
    numerators, total, _ = _dressed_numerators(
        model, channel, endpoint_kernel, coarse_pair, configuration
    )
    return {element: mass / total for element, mass in numerators.items()}


def dressed_transport_law(
    model: FalsificationModel,
    channel: str,
    endpoint_kernel: EndpointKernel,
    coarse_pair: tuple[str, str],
    configuration: str = "uniform",
) -> dict[int, float]:
    """Return the conditional law of dressed transports on one coarse pair.

    The law is a distribution on the structure group, not a mean, and it is the
    exact coarse connection datum. Every group element is listed so that the result
    is a full law on the group; the atoms are the elements of positive mass.
    """
    exact = exact_dressed_transport_law(
        model, channel, endpoint_kernel, coarse_pair, configuration
    )
    return {element: float(mass) for element, mass in exact.items()}


def restricted_dressed_mass(
    model: FalsificationModel,
    channel: str,
    endpoint_kernel: EndpointKernel,
    coarse_pair: tuple[str, str],
    configuration: str = "uniform",
) -> Fraction:
    """Return the total mass of the restricted dressed numerator, a negative control.

    The restricted numerator sums the edge event law over the pairs whose receiver
    has positive membership in the left label and whose source has positive
    membership in the right label, dropping the endpoint kernel that the denominator
    carries. Under a hard assignment the dropped factor is the indicator that is
    identically one on that index set and the total is one; under the soft
    memberships declared here the two disagree and the restricted object is not a
    probability measure. The value is exact, so a departure from one is a fact about
    the formula and not a rounding artifact.
    """
    _, total, restricted = _dressed_numerators(
        model, channel, endpoint_kernel, coarse_pair, configuration
    )
    return restricted / total


def positive_atoms(law: Mapping[int, float]) -> tuple[int, ...]:
    """Return the group elements carrying positive mass, in sorted order."""
    return tuple(sorted(element for element, mass in law.items() if mass > 0))


def stabilizer_mass(
    law: Mapping[int, float],
    representation: CyclicRepresentation,
    target: Law,
) -> float:
    """Return the mass a transport law places on the stabilizer of a target law.

    The coarse criterion is that this mass equals one. It is a mass statement, not a
    support containment statement: support and closedness presuppose a topology on
    the structure group that the measurable tier of the construction never declares,
    while the stabilizer is a measurable subgroup as soon as the action is jointly
    measurable. The two formulations agree only after a topological group and a
    continuous action are separately declared.
    """
    total = 0.0
    for element, mass in law.items():
        if representation.fixes(element, target):
            total += float(mass)
    return total


def _permutation_matrix(representation: CyclicRepresentation, element: int) -> np.ndarray:
    """Return the pushforward matrix of one group element acting on column laws."""
    order = representation.order
    matrix = np.zeros((order, order), dtype=np.float64)
    permutation = representation.permutation(element)
    for source in range(order):
        matrix[permutation[source], source] = 1.0
    return matrix


def dressed_barycenter(
    law: Mapping[int, float],
    representation: CyclicRepresentation,
) -> np.ndarray:
    """Return the mixture of permutation matrices weighted by a dressed transport law."""
    order = representation.order
    matrix = np.zeros((order, order), dtype=np.float64)
    for element, mass in law.items():
        matrix += float(mass) * _permutation_matrix(representation, element)
    return matrix


def barycenter_is_group_element(
    barycenter: np.ndarray,
    representation: CyclicRepresentation,
    tolerance: float = 1e-12,
) -> bool:
    """Report whether a barycenter coincides with the image of a group element.

    A mixture of permutation matrices is doubly stochastic but is generically not a
    permutation matrix, so the coarse edge transport does not exist as a single
    group element. This predicate is the guard: a barycenter that fails it must
    never be composed, inverted, or used as a transport anywhere.
    """
    for element in range(representation.order):
        candidate = _permutation_matrix(representation, element)
        if np.allclose(barycenter, candidate, atol=tolerance, rtol=0.0):
            return True
    return False


def composite_transport_law(
    joint: Mapping[tuple[int, int], float],
    order: int = GROUP_ORDER,
) -> dict[int, float]:
    """Return the pushforward of a joint mark law under group multiplication.

    This is the forward direction of the composition proposition and the only
    direction that holds. The composite law of two consecutive dressed transports is
    always the pushforward of their joint law; it reduces to the convolution of the
    marginals exactly when the joint is a product, and the reduction is not
    reversible.
    """
    result = {element: 0.0 for element in range(order)}
    for (left, right), mass in joint.items():
        if type(left) is not int or type(right) is not int:
            raise TypeError("joint keys must be pairs of group elements")
        result[(left + right) % order] += float(mass)
    return result


def convolve(
    left: Mapping[int, float],
    right: Mapping[int, float],
    order: int = GROUP_ORDER,
) -> dict[int, float]:
    """Return the ordered convolution of two laws on the structure group."""
    result = {element: 0.0 for element in range(order)}
    for first, left_mass in left.items():
        for second, right_mass in right.items():
            result[(first + second) % order] += float(left_mass) * float(right_mass)
    return result


@dataclass(frozen=True)
class ConvolutionWitness:
    """The witness that convolution equality does not detect mark dependence."""

    joint: dict[tuple[int, int], float]
    product_joint: dict[tuple[int, int], float]
    left_marginal: dict[int, float]
    right_marginal: dict[int, float]
    composite: dict[int, float]
    convolution: dict[int, float]
    composite_matches_convolution: bool
    joint_is_a_product: bool


def convolution_converse_witness(order: int = GROUP_ORDER) -> ConvolutionWitness:
    """Return the maximally dependent pair whose composite still equals the convolution.

    Take the first mark uniform on the cyclic group and the second mark equal to it.
    The pair is as dependent as a pair can be, yet the sum is uniform whenever
    doubling is invertible, and the convolution of the two uniform marginals is
    uniform as well. So the composite law agrees with the convolution while the joint
    is not a product, and convolution equality is useless as a test of independence.
    """
    if math.gcd(2, order) != 1:
        raise ValueError("the witness needs doubling to be invertible in the group")
    mass = 1.0 / order
    joint = {(element, element): mass for element in range(order)}
    left_marginal = {element: mass for element in range(order)}
    right_marginal = {element: mass for element in range(order)}
    product_joint = {
        (first, second): left_marginal[first] * right_marginal[second]
        for first in range(order)
        for second in range(order)
    }
    composite = composite_transport_law(joint, order)
    convolution = convolve(left_marginal, right_marginal, order)
    matches = all(
        math.isclose(composite[element], convolution[element], rel_tol=0.0, abs_tol=1e-15)
        for element in range(order)
    )
    is_product = all(
        math.isclose(
            joint.get(key, 0.0), product_joint[key], rel_tol=0.0, abs_tol=1e-15
        )
        for key in product_joint
    )
    return ConvolutionWitness(
        joint=joint,
        product_joint=product_joint,
        left_marginal=left_marginal,
        right_marginal=right_marginal,
        composite=composite,
        convolution=convolution,
        composite_matches_convolution=matches,
        joint_is_a_product=is_product,
    )


@dataclass(frozen=True)
class BlockRetentionRow:
    """One measured block, channel, and admitted family."""

    partition: Partition
    block: tuple[int, ...]
    channel: str
    admitted: str
    components: int
    holonomy: tuple[int, ...]
    fixed_sector_size: int
    distortion: float
    zero_attainable: bool


def retention_report(
    model: FalsificationModel,
    states: Mapping[int, int] | None = None,
) -> tuple[BlockRetentionRow, ...]:
    """Return one measured row per candidate block, channel, and admitted family."""
    configuration = dict(reference_states(model)) if states is None else dict(states)
    rows: list[BlockRetentionRow] = []
    for partition in model.candidate_partitions:
        for block in partition:
            for channel in CHANNELS:
                for admitted in ADMITTED_FAMILIES:
                    sector = fixed_sector(model, block, channel, admitted)
                    rows.append(
                        BlockRetentionRow(
                            partition=partition,
                            block=tuple(block),
                            channel=channel,
                            admitted=admitted,
                            components=len(block_components(model, block)),
                            holonomy=block_holonomy_group(model, block, channel),
                            fixed_sector_size=len(sector),
                            distortion=holonomy_distortion(
                                model, block, channel, admitted, configuration
                            ),
                            zero_attainable=zero_distortion_is_attainable(
                                model, block, channel, admitted
                            ),
                        )
                    )
    return tuple(rows)


@dataclass(frozen=True)
class PredictionReport:
    """The pre-registered predictions of the holonomy retention measurement."""

    cyclic_block: tuple[int, ...]
    flat_block: tuple[int, ...]
    belief_cyclic_orbit: float
    belief_cyclic_simplex: float
    belief_cyclic_zero_attainable: bool
    model_cyclic_zero_states: dict[int, int]
    model_cyclic_zero_distortion: float
    flat_block_belief_zero_distortion: float
    flat_block_model_zero_distortion: float
    belief_positive_on_cyclic_block: bool
    model_can_vanish_on_cyclic_block: bool
    both_can_vanish_on_flat_block: bool


def prediction_report(model: FalsificationModel) -> PredictionReport:
    """Return the measured verdicts on the three declared retention predictions."""
    cyclic = (1, 2, 3)
    flat = (4, 5, 6)
    states = reference_states(model)
    model_target = _family(model, "model")[0]
    model_states = aligned_state_configuration(model, cyclic, "model", model_target)
    belief_target = _family(model, "belief")[0]
    flat_belief_states = aligned_state_configuration(model, flat, "belief", belief_target)
    flat_model_states = aligned_state_configuration(model, flat, "model", model_target)
    belief_orbit = holonomy_distortion(model, cyclic, "belief", "orbit", states)
    belief_simplex = holonomy_distortion(model, cyclic, "belief", "simplex", states)
    model_zero = holonomy_distortion(model, cyclic, "model", "orbit", model_states)
    flat_belief_zero = holonomy_distortion(model, flat, "belief", "orbit", flat_belief_states)
    flat_model_zero = holonomy_distortion(model, flat, "model", "orbit", flat_model_states)
    return PredictionReport(
        cyclic_block=cyclic,
        flat_block=flat,
        belief_cyclic_orbit=belief_orbit,
        belief_cyclic_simplex=belief_simplex,
        belief_cyclic_zero_attainable=zero_distortion_is_attainable(
            model, cyclic, "belief", "simplex"
        ),
        model_cyclic_zero_states=model_states,
        model_cyclic_zero_distortion=model_zero,
        flat_block_belief_zero_distortion=flat_belief_zero,
        flat_block_model_zero_distortion=flat_model_zero,
        belief_positive_on_cyclic_block=bool(belief_orbit > 0.0 and belief_simplex > 0.0),
        model_can_vanish_on_cyclic_block=bool(model_zero == 0.0),
        both_can_vanish_on_flat_block=bool(flat_belief_zero == 0.0 and flat_model_zero == 0.0),
    )


@dataclass(frozen=True)
class FalsifierVerdict:
    """The pre-registered theory falsifier of the holonomy retention measurement."""

    positive_at_declared_states: bool
    zero_distortion_blocks: tuple[tuple[tuple[int, ...], str], ...]
    fired: bool


def theory_falsifier_verdict(
    model: FalsificationModel,
    states: Mapping[int, int] | None = None,
) -> FalsifierVerdict:
    """Return whether no zero-distortion belief parent exists on any candidate block.

    Two readings are reported and neither is allowed to stand in for the other. The
    first is whether every candidate block has a strictly positive belief score at
    the declared state configuration, which is a statement about one configuration.
    The second, which is what the falsifier means, is whether no candidate block
    admits a zero-distortion belief parent under any state configuration and either
    admitted family. The falsifier fires only on the second.
    """
    configuration = dict(reference_states(model)) if states is None else dict(states)
    blocks: list[tuple[tuple[int, ...], str]] = []
    positive = True
    for partition in model.candidate_partitions:
        for block in partition:
            for admitted in ADMITTED_FAMILIES:
                if holonomy_distortion(model, block, "belief", admitted, configuration) <= 0.0:
                    positive = False
                if zero_distortion_is_attainable(model, block, "belief", admitted):
                    blocks.append((tuple(block), admitted))
    return FalsifierVerdict(
        positive_at_declared_states=positive,
        zero_distortion_blocks=tuple(blocks),
        fired=not blocks,
    )


@dataclass(frozen=True)
class LogicalChainReport:
    """The three logical-chain links, each exhibited or honestly declared absent."""

    flat_block: tuple[int, ...]
    flat_channel: str
    flat_holonomy: tuple[int, ...]
    flat_loop_law: dict[int, float]
    flatness_implies_stabilization: bool
    minimum_flat_stabilizer_mass: float
    disagreement_block: tuple[int, ...]
    disagreement_distortion: float
    flatness_implies_agreement: bool
    stabilization_without_flatness_in_orbit_family: bool
    curved_block: tuple[int, ...]
    curved_holonomy: tuple[int, ...]
    curved_loop_law: dict[int, float]
    uniform_stabilizer_mass: float
    stabilization_without_flatness_on_uniform: bool


def logical_chain_report(model: FalsificationModel) -> LogicalChainReport:
    """Return the executable checks on the three implications between the criteria.

    Flatness implies stabilization trivially, because a trivial holonomy group
    contains only the identity and the identity fixes every law; the measurable-tier
    version is that the coarse loop law is a point mass at the identity, so it puts
    mass one on every stabilizer. Flatness does not imply agreement: two agents
    joined by an identity transport but holding different presentations have a
    strictly positive score. Stabilization does not imply flatness in general, but
    inside this model no nontrivial cyclic shift stabilizes any non-uniform law, so
    no witness exists in the orbit family; the witness is supplied on the uniform
    law of the simplex family, which every group element fixes while the belief
    connection carries nontrivial holonomy.
    """
    kernel = declared_endpoint_kernel(model)
    flat_block = kernel.block(model.parent_labels[0])
    flat_holonomy = block_holonomy_group(model, flat_block, "model")
    flat_law = dressed_transport_law(model, "model", kernel, (model.parent_labels[0],) * 2)
    representation = _representation(model, "model")
    masses = [
        stabilizer_mass(flat_law, representation, law) for law in _family(model, "model")
    ]
    group_level = all(
        representation.fixes(element, law)
        for element in flat_holonomy
        for law in _family(model, "model")
    )
    disagreement_block = (3, 4)
    belief_family = _family(model, "belief")
    disagreement_states = {
        3: _state_index(model, "belief", belief_family[0]),
        4: _state_index(model, "belief", belief_family[1]),
    }
    disagreement = holonomy_distortion(
        model, disagreement_block, "belief", "orbit", disagreement_states
    )
    orbit_witness = False
    for partition in model.candidate_partitions:
        for block in partition:
            for channel in CHANNELS:
                holonomy = block_holonomy_group(model, block, channel)
                if holonomy == (0,):
                    continue
                sector = fixed_sector(model, block, channel, "orbit")
                if sector:
                    orbit_witness = True
    curved_block = kernel.block(model.parent_labels[0])
    curved_holonomy = block_holonomy_group(model, curved_block, "belief")
    curved_law = dressed_transport_law(model, "belief", kernel, (model.parent_labels[0],) * 2)
    uniform_mass = stabilizer_mass(
        curved_law, _representation(model, "belief"), uniform_law(model.graph.order)
    )
    return LogicalChainReport(
        flat_block=flat_block,
        flat_channel="model",
        flat_holonomy=flat_holonomy,
        flat_loop_law=flat_law,
        flatness_implies_stabilization=bool(group_level and min(masses) == 1.0),
        minimum_flat_stabilizer_mass=min(masses),
        disagreement_block=disagreement_block,
        disagreement_distortion=disagreement,
        flatness_implies_agreement=bool(disagreement <= 0.0),
        stabilization_without_flatness_in_orbit_family=orbit_witness,
        curved_block=curved_block,
        curved_holonomy=curved_holonomy,
        curved_loop_law=curved_law,
        uniform_stabilizer_mass=uniform_mass,
        stabilization_without_flatness_on_uniform=bool(
            curved_holonomy != (0,) and uniform_mass == 1.0
        ),
    )


__all__ = [
    "ADMITTED_FAMILIES",
    "CHANNELS",
    "REFERENCE_STATE_INDICES",
    "BlockRetentionRow",
    "ConvolutionWitness",
    "EndpointKernel",
    "FalsifierVerdict",
    "LogicalChainReport",
    "PredictionReport",
    "aligned_state_configuration",
    "barycenter_is_group_element",
    "block_components",
    "block_holonomy_group",
    "block_transport_elements",
    "composite_transport_law",
    "convolution_converse_witness",
    "convolve",
    "declared_endpoint_kernel",
    "dressed_barycenter",
    "dressed_transport_law",
    "exact_dressed_transport_law",
    "fixed_sector",
    "holonomy_distortion",
    "logical_chain_report",
    "positive_atoms",
    "prediction_report",
    "reference_states",
    "restricted_dressed_mass",
    "retention_report",
    "stabilizer_mass",
    "theory_falsifier_verdict",
    "transported_laws",
    "zero_distortion_is_attainable",
]
