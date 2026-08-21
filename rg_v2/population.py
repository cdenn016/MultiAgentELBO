"""Exact local-to-population construction for the RG-v2 laboratory."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json

from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.contracts import AgentDatum, ModelEvaluation, PopulationJoint, RecordDatum


_MAX_LATENT_STATES = 4096


def _compact_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))


def _decode_local_label(label: str) -> tuple[str, str]:
    try:
        value = json.loads(label)
    except (TypeError, json.JSONDecodeError) as error:
        raise ValueError("local state labels must be canonical JSON pairs") from error
    if (
        not isinstance(value, list)
        or len(value) != 2
        or any(not isinstance(item, str) or not item for item in value)
        or _compact_json(value) != label
    ):
        raise ValueError("local state labels must be canonical JSON pairs")
    return value[0], value[1]


def _expected_assignment_labels(
    ids: tuple[str, ...],
    agents_by_id: dict[str, AgentDatum],
) -> tuple[str, ...]:
    supports = tuple(tuple(_decode_local_label(label) for label in agents_by_id[agent_id].state_labels) for agent_id in ids)
    return tuple(
        _compact_json([[agent_id, belief, model] for agent_id, (belief, model) in zip(ids, states, strict=True)])
        for states in product(*supports)
    )


def _validate_exact_channel(
    channel: ExactMarkovChannel,
    source_labels: tuple[str, ...],
    target_labels: tuple[str, ...],
    field: str,
) -> None:
    if not isinstance(channel, ExactMarkovChannel):
        raise TypeError(f"{field} must be an ExactMarkovChannel")
    if channel.recognition_independent is not True:
        raise ValueError(f"{field} must be recognition-independent")
    if channel.source_labels != source_labels:
        raise ValueError(f"{field} source support must equal the complete canonical support")
    if channel.target_labels != target_labels:
        raise ValueError(f"{field} target support must equal the declared support")
    if not isinstance(channel.matrix, tuple) or len(channel.matrix) != len(source_labels):
        raise ValueError(f"{field} rows must align with the source support")
    for row in channel.matrix:
        if not isinstance(row, tuple) or len(row) != len(target_labels):
            raise ValueError(f"{field} columns must align with the target support")
        if any(not isinstance(value, Fraction) for value in row):
            raise TypeError(f"{field} entries must be exact Fraction values")
        if any(value < 0 for value in row) or sum(row, Fraction(0)) != 1:
            raise ValueError(f"{field} rows must be nonnegative and normalized exactly")


def _validate_evaluator_compatibility(
    agent: AgentDatum,
    parent_labels: tuple[str, ...],
) -> None:
    if not isinstance(agent.evaluator, tuple) or len(agent.evaluator) != len(agent.model_labels):
        raise ValueError("agent evaluator must contain every model label exactly once")
    if any(not isinstance(entry, ModelEvaluation) for entry in agent.evaluator):
        raise TypeError("agent evaluator entries must be ModelEvaluation values")
    if tuple(entry.model_label for entry in agent.evaluator) != agent.model_labels:
        raise ValueError("agent evaluator labels must equal model labels in order")
    for entry in agent.evaluator:
        _validate_exact_channel(entry.kernel, parent_labels, agent.belief_labels, "agent evaluator kernel")

    model_count = len(agent.model_labels)
    for source_index, row in enumerate(agent.generative_kernel.matrix):
        for model_index, model_label in enumerate(agent.model_labels):
            state_indices = tuple(belief_index * model_count + model_index for belief_index in range(len(agent.belief_labels)))
            model_mass = sum((row[index] for index in state_indices), Fraction(0))
            if model_mass == 0:
                continue
            conditional = tuple(row[index] / model_mass for index in state_indices)
            if conditional != agent.evaluator[model_index].kernel.matrix[source_index]:
                raise ValueError(f"agent evaluator is incompatible with positive generative model slice {model_label!r}")


def _validate_agent_dag(agents: tuple[AgentDatum, ...]) -> tuple[str, ...]:
    if not isinstance(agents, tuple) or not agents:
        raise ValueError("agents must be a nonempty tuple")
    if any(not isinstance(agent, AgentDatum) for agent in agents):
        raise TypeError("agents must contain only AgentDatum values")

    agent_order = tuple(agent.agent_id for agent in agents)
    if any(not isinstance(agent_id, str) or not agent_id for agent_id in agent_order):
        raise ValueError("agent IDs must be nonempty strings")
    if len(set(agent_order)) != len(agent_order):
        raise ValueError("agent IDs must be unique")

    agents_by_id: dict[str, AgentDatum] = {}
    latent_count = 1
    for agent in agents:
        if not isinstance(agent.parent_ids, tuple) or len(set(agent.parent_ids)) != len(agent.parent_ids):
            raise ValueError("parent IDs must be a unique tuple")
        if agent.agent_id in agent.parent_ids:
            raise ValueError("an agent cannot be its own parent")
        if any(parent_id not in agents_by_id for parent_id in agent.parent_ids):
            raise ValueError("agents must appear in declared topological order")
        if (
            not isinstance(agent.belief_labels, tuple)
            or not agent.belief_labels
            or len(set(agent.belief_labels)) != len(agent.belief_labels)
            or any(not isinstance(label, str) or not label for label in agent.belief_labels)
        ):
            raise ValueError("belief labels must be nonempty and unique")
        if (
            not isinstance(agent.model_labels, tuple)
            or not agent.model_labels
            or len(set(agent.model_labels)) != len(agent.model_labels)
            or any(not isinstance(label, str) or not label for label in agent.model_labels)
        ):
            raise ValueError("model labels must be nonempty and unique")
        canonical_states = tuple(_compact_json([belief, model]) for belief in agent.belief_labels for model in agent.model_labels)
        if agent.state_labels != canonical_states:
            raise ValueError("agent state support must be the canonical belief-major Cartesian product")
        parent_labels = ("()",) if not agent.parent_ids else _expected_assignment_labels(agent.parent_ids, agents_by_id)
        _validate_exact_channel(agent.generative_kernel, parent_labels, agent.state_labels, "agent generative kernel")
        _validate_evaluator_compatibility(agent, parent_labels)
        agents_by_id[agent.agent_id] = agent
        latent_count *= len(agent.state_labels)
        if latent_count > _MAX_LATENT_STATES:
            raise ValueError(f"population exceeds the {_MAX_LATENT_STATES}-state exact limit")
    return agent_order


def _validate_record_ownership(
    records: tuple[RecordDatum, ...],
    agents: tuple[AgentDatum, ...],
) -> None:
    if not isinstance(records, tuple) or not records:
        raise ValueError("records must be a nonempty tuple")
    if any(not isinstance(record, RecordDatum) for record in records):
        raise TypeError("records must contain only RecordDatum values")
    record_ids = tuple(record.record_id for record in records)
    if any(not isinstance(record_id, str) or not record_id for record_id in record_ids):
        raise ValueError("record IDs must be nonempty strings")
    if len(set(record_ids)) != len(record_ids):
        raise ValueError("record IDs must be unique")

    agents_by_id = {agent.agent_id: agent for agent in agents}
    for record in records:
        if not isinstance(record.owner_id, str) or not record.owner_id:
            raise ValueError("record owner must be a nonempty agent ID")
        if (
            not isinstance(record.scope_ids, tuple)
            or not record.scope_ids
            or len(set(record.scope_ids)) != len(record.scope_ids)
            or any(not isinstance(agent_id, str) or not agent_id for agent_id in record.scope_ids)
        ):
            raise ValueError("record scope must be nonempty and unique")
        if record.owner_id not in record.scope_ids:
            raise ValueError("record owner must belong to its declared scope")
        if any(agent_id not in agents_by_id for agent_id in record.scope_ids):
            raise ValueError("record scope agents must be declared population agents")
        if (
            not isinstance(record.outcome_labels, tuple)
            or not record.outcome_labels
            or len(set(record.outcome_labels)) != len(record.outcome_labels)
            or any(not isinstance(label, str) or not label for label in record.outcome_labels)
        ):
            raise ValueError("record outcome labels must be nonempty and unique")
        source_labels = _expected_assignment_labels(record.scope_ids, agents_by_id)
        _validate_exact_channel(record.kernel, source_labels, record.outcome_labels, "record kernel")


def _canonical_latent_labels(agents: tuple[AgentDatum, ...]) -> tuple[str, ...]:
    return tuple(
        _compact_json(
            [
                [agent.agent_id, *_decode_local_label(state_label)]
                for agent, state_label in zip(agents, state_labels, strict=True)
            ]
        )
        for state_labels in product(*(agent.state_labels for agent in agents))
    )


def _canonical_observation_labels(records: tuple[RecordDatum, ...]) -> tuple[str, ...]:
    return tuple(
        _compact_json([[record.record_id, outcome] for record, outcome in zip(records, outcomes, strict=True)])
        for outcomes in product(*(record.outcome_labels for record in records))
    )


def _multiply_each_factor_once(
    agents: tuple[AgentDatum, ...],
    records: tuple[RecordDatum, ...],
    latent_labels: tuple[str, ...],
    observation_labels: tuple[str, ...],
) -> tuple[tuple[Fraction, ...], ...]:
    agent_maps = {
        agent.agent_id: (
            {label: index for index, label in enumerate(agent.generative_kernel.source_labels)},
            {label: index for index, label in enumerate(agent.state_labels)},
        )
        for agent in agents
    }
    record_maps = {
        record.record_id: (
            {label: index for index, label in enumerate(record.kernel.source_labels)},
            {label: index for index, label in enumerate(record.outcome_labels)},
        )
        for record in records
    }

    rows: list[tuple[Fraction, ...]] = []
    for latent_label in latent_labels:
        decoded_latent = json.loads(latent_label)
        latent_by_id = {item[0]: (item[1], item[2]) for item in decoded_latent}
        generative_mass = Fraction(1)
        for agent in agents:
            source_label = "()" if not agent.parent_ids else _compact_json([[parent_id, *latent_by_id[parent_id]] for parent_id in agent.parent_ids])
            target_label = _compact_json(list(latent_by_id[agent.agent_id]))
            source_index = agent_maps[agent.agent_id][0][source_label]
            target_index = agent_maps[agent.agent_id][1][target_label]
            generative_mass *= agent.generative_kernel.matrix[source_index][target_index]

        row: list[Fraction] = []
        for observation_label in observation_labels:
            decoded_observation = json.loads(observation_label)
            observation_by_id = {item[0]: item[1] for item in decoded_observation}
            mass = generative_mass
            for record in records:
                source_label = _compact_json([[agent_id, *latent_by_id[agent_id]] for agent_id in record.scope_ids])
                source_index = record_maps[record.record_id][0][source_label]
                target_index = record_maps[record.record_id][1][observation_by_id[record.record_id]]
                mass *= record.kernel.matrix[source_index][target_index]
            row.append(mass)
        rows.append(tuple(row))
    return tuple(rows)


def _sum_matrix(masses: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    return sum((sum(row, Fraction(0)) for row in masses), Fraction(0))


def construct_population_joint(
    agents: tuple[AgentDatum, ...],
    records: tuple[RecordDatum, ...],
    context_id: str,
) -> PopulationJoint:
    """Construct ``P_V(y_V, x_V)`` from each local factor exactly once."""
    if not isinstance(context_id, str) or not context_id:
        raise ValueError("context ID must be a nonempty string")
    agent_order = _validate_agent_dag(agents)
    _validate_record_ownership(records, agents)
    latent_labels = _canonical_latent_labels(agents)
    observation_labels = _canonical_observation_labels(records)
    masses = _multiply_each_factor_once(agents, records, latent_labels, observation_labels)
    if _sum_matrix(masses) != Fraction(1):
        raise ArithmeticError("constructed population joint is not normalized")
    trace = tuple(f"agent:{item}" for item in agent_order) + tuple(f"record:{item.record_id}" for item in records)
    return PopulationJoint(
        context_id=context_id,
        agent_order=agent_order,
        record_order=tuple(item.record_id for item in records),
        latent_labels=latent_labels,
        observation_labels=observation_labels,
        joint_masses=masses,
        construction_trace=trace,
    )


def enumerate_population_joint_independently(
    agents: tuple[AgentDatum, ...],
    records: tuple[RecordDatum, ...],
    context_id: str,
) -> PopulationJoint:
    """Independently enumerate the complete population law from public fields.

    This oracle deliberately duplicates validation, support construction, row
    lookup, factor multiplication, normalization, and trace assembly. It does
    not call the primary constructor or any of its private helpers.
    """
    if not isinstance(context_id, str) or not context_id:
        raise ValueError("context ID must be a nonempty string")
    if not isinstance(agents, tuple) or not agents:
        raise ValueError("agents must be a nonempty tuple")
    if any(not isinstance(agent, AgentDatum) for agent in agents):
        raise TypeError("agents must contain only AgentDatum values")

    ordered_agents: dict[str, AgentDatum] = {}
    latent_count = 1
    for agent in agents:
        if not isinstance(agent.agent_id, str) or not agent.agent_id or agent.agent_id in ordered_agents:
            raise ValueError("independent oracle requires unique nonempty agent IDs")
        if not isinstance(agent.parent_ids, tuple) or len(set(agent.parent_ids)) != len(agent.parent_ids):
            raise ValueError("independent oracle requires unique parent IDs")
        if agent.agent_id in agent.parent_ids or any(parent_id not in ordered_agents for parent_id in agent.parent_ids):
            raise ValueError("independent oracle requires declared topological agent order")
        for support_name, labels in (("belief", agent.belief_labels), ("model", agent.model_labels)):
            if (
                not isinstance(labels, tuple)
                or not labels
                or len(set(labels)) != len(labels)
                or any(not isinstance(label, str) or not label for label in labels)
            ):
                raise ValueError(f"independent oracle requires unique nonempty {support_name} labels")
        expected_states = tuple(
            json.dumps([belief, model], ensure_ascii=True, separators=(",", ":"))
            for belief in agent.belief_labels
            for model in agent.model_labels
        )
        if agent.state_labels != expected_states:
            raise ValueError("independent oracle requires the canonical local state support")

        if not agent.parent_ids:
            expected_sources = ("()",)
        else:
            parent_supports: list[tuple[tuple[str, str], ...]] = []
            for parent_id in agent.parent_ids:
                parent_states: list[tuple[str, str]] = []
                for label in ordered_agents[parent_id].state_labels:
                    try:
                        decoded = json.loads(label)
                    except (TypeError, json.JSONDecodeError) as error:
                        raise ValueError("independent oracle found a noncanonical parent state") from error
                    if (
                        not isinstance(decoded, list)
                        or len(decoded) != 2
                        or any(not isinstance(item, str) or not item for item in decoded)
                        or json.dumps(decoded, ensure_ascii=True, separators=(",", ":")) != label
                    ):
                        raise ValueError("independent oracle found a noncanonical parent state")
                    parent_states.append((decoded[0], decoded[1]))
                parent_supports.append(tuple(parent_states))
            expected_sources = tuple(
                json.dumps(
                    [[parent_id, state[0], state[1]] for parent_id, state in zip(agent.parent_ids, parent_states, strict=True)],
                    ensure_ascii=True,
                    separators=(",", ":"),
                )
                for parent_states in product(*parent_supports)
            )

        generative = agent.generative_kernel
        if not isinstance(generative, ExactMarkovChannel):
            raise TypeError("independent oracle requires exact generative channels")
        if generative.recognition_independent is not True:
            raise ValueError("independent oracle requires recognition-independent generative channels")
        if generative.source_labels != expected_sources or generative.target_labels != agent.state_labels:
            raise ValueError("independent oracle found incompatible generative support")
        if not isinstance(generative.matrix, tuple) or len(generative.matrix) != len(expected_sources):
            raise ValueError("independent oracle found incompatible generative rows")
        for row in generative.matrix:
            if not isinstance(row, tuple) or len(row) != len(agent.state_labels):
                raise ValueError("independent oracle found incompatible generative columns")
            if any(not isinstance(value, Fraction) for value in row):
                raise TypeError("independent oracle requires exact generative entries")
            if any(value < 0 for value in row) or sum(row, Fraction(0)) != 1:
                raise ValueError("independent oracle requires normalized generative rows")

        if not isinstance(agent.evaluator, tuple) or len(agent.evaluator) != len(agent.model_labels):
            raise ValueError("independent oracle requires one evaluator per model")
        if any(not isinstance(entry, ModelEvaluation) for entry in agent.evaluator):
            raise TypeError("independent oracle requires ModelEvaluation entries")
        if tuple(entry.model_label for entry in agent.evaluator) != agent.model_labels:
            raise ValueError("independent oracle found misordered evaluator labels")
        for entry in agent.evaluator:
            evaluator_kernel = entry.kernel
            if not isinstance(evaluator_kernel, ExactMarkovChannel):
                raise TypeError("independent oracle requires exact evaluator kernels")
            if (
                evaluator_kernel.recognition_independent is not True
                or evaluator_kernel.source_labels != expected_sources
                or evaluator_kernel.target_labels != agent.belief_labels
            ):
                raise ValueError("independent oracle found incompatible evaluator support")
            if not isinstance(evaluator_kernel.matrix, tuple) or len(evaluator_kernel.matrix) != len(expected_sources):
                raise ValueError("independent oracle found incompatible evaluator rows")
            for row in evaluator_kernel.matrix:
                if not isinstance(row, tuple) or len(row) != len(agent.belief_labels):
                    raise ValueError("independent oracle found incompatible evaluator columns")
                if any(not isinstance(value, Fraction) for value in row):
                    raise TypeError("independent oracle requires exact evaluator entries")
                if any(value < 0 for value in row) or sum(row, Fraction(0)) != 1:
                    raise ValueError("independent oracle requires normalized evaluator rows")
        model_count = len(agent.model_labels)
        for source_index, generative_row in enumerate(generative.matrix):
            for model_index, model_label in enumerate(agent.model_labels):
                state_indices = tuple(belief_index * model_count + model_index for belief_index in range(len(agent.belief_labels)))
                model_mass = sum((generative_row[index] for index in state_indices), Fraction(0))
                if model_mass != 0:
                    conditional = tuple(generative_row[index] / model_mass for index in state_indices)
                    if conditional != agent.evaluator[model_index].kernel.matrix[source_index]:
                        raise ValueError(f"independent oracle found evaluator-incompatible model slice {model_label!r}")
        ordered_agents[agent.agent_id] = agent
        latent_count *= len(agent.state_labels)
        if latent_count > _MAX_LATENT_STATES:
            raise ValueError(f"independent oracle exceeds the {_MAX_LATENT_STATES}-state exact limit")

    if not isinstance(records, tuple) or not records:
        raise ValueError("records must be a nonempty tuple")
    if any(not isinstance(record, RecordDatum) for record in records):
        raise TypeError("records must contain only RecordDatum values")
    record_ids = tuple(record.record_id for record in records)
    if any(not isinstance(record_id, str) or not record_id for record_id in record_ids) or len(set(record_ids)) != len(record_ids):
        raise ValueError("independent oracle requires unique nonempty record IDs")
    for record in records:
        if not isinstance(record.owner_id, str) or not record.owner_id:
            raise ValueError("independent oracle requires a record owner")
        if (
            not isinstance(record.scope_ids, tuple)
            or not record.scope_ids
            or len(set(record.scope_ids)) != len(record.scope_ids)
            or any(not isinstance(agent_id, str) or not agent_id for agent_id in record.scope_ids)
        ):
            raise ValueError("independent oracle requires a unique nonempty record scope")
        if record.owner_id not in record.scope_ids:
            raise ValueError("independent oracle requires the record owner in scope")
        if any(agent_id not in ordered_agents for agent_id in record.scope_ids):
            raise ValueError("independent oracle requires declared record-scope agents")
        if (
            not isinstance(record.outcome_labels, tuple)
            or not record.outcome_labels
            or len(set(record.outcome_labels)) != len(record.outcome_labels)
            or any(not isinstance(label, str) or not label for label in record.outcome_labels)
        ):
            raise ValueError("independent oracle requires unique nonempty record outcomes")

        scope_supports: list[tuple[tuple[str, str], ...]] = []
        for agent_id in record.scope_ids:
            local_states: list[tuple[str, str]] = []
            for label in ordered_agents[agent_id].state_labels:
                try:
                    decoded = json.loads(label)
                except (TypeError, json.JSONDecodeError) as error:
                    raise ValueError("independent oracle found a noncanonical record-scope state") from error
                if (
                    not isinstance(decoded, list)
                    or len(decoded) != 2
                    or any(not isinstance(item, str) or not item for item in decoded)
                    or json.dumps(decoded, ensure_ascii=True, separators=(",", ":")) != label
                ):
                    raise ValueError("independent oracle found a noncanonical record-scope state")
                local_states.append((decoded[0], decoded[1]))
            scope_supports.append(tuple(local_states))
        expected_record_sources = tuple(
            json.dumps(
                [[agent_id, state[0], state[1]] for agent_id, state in zip(record.scope_ids, scoped_states, strict=True)],
                ensure_ascii=True,
                separators=(",", ":"),
            )
            for scoped_states in product(*scope_supports)
        )
        record_kernel = record.kernel
        if not isinstance(record_kernel, ExactMarkovChannel):
            raise TypeError("independent oracle requires exact record kernels")
        if record_kernel.recognition_independent is not True:
            raise ValueError("independent oracle requires recognition-independent record kernels")
        if record_kernel.source_labels != expected_record_sources or record_kernel.target_labels != record.outcome_labels:
            raise ValueError("independent oracle found incompatible record support")
        if not isinstance(record_kernel.matrix, tuple) or len(record_kernel.matrix) != len(expected_record_sources):
            raise ValueError("independent oracle found incompatible record rows")
        for row in record_kernel.matrix:
            if not isinstance(row, tuple) or len(row) != len(record.outcome_labels):
                raise ValueError("independent oracle found incompatible record columns")
            if any(not isinstance(value, Fraction) for value in row):
                raise TypeError("independent oracle requires exact record entries")
            if any(value < 0 for value in row) or sum(row, Fraction(0)) != 1:
                raise ValueError("independent oracle requires normalized record rows")

    agent_order = tuple(agent.agent_id for agent in agents)
    latent_labels_list: list[str] = []
    latent_index_rows: list[tuple[int, ...]] = []
    for state_indices in product(*(range(len(agent.state_labels)) for agent in agents)):
        assignment: list[list[str]] = []
        for agent, state_index in zip(agents, state_indices, strict=True):
            decoded = json.loads(agent.state_labels[state_index])
            assignment.append([agent.agent_id, decoded[0], decoded[1]])
        latent_labels_list.append(json.dumps(assignment, ensure_ascii=True, separators=(",", ":")))
        latent_index_rows.append(tuple(state_indices))

    observation_labels_list: list[str] = []
    observation_index_rows: list[tuple[int, ...]] = []
    for outcome_indices in product(*(range(len(record.outcome_labels)) for record in records)):
        assignment = [
            [record.record_id, record.outcome_labels[outcome_index]]
            for record, outcome_index in zip(records, outcome_indices, strict=True)
        ]
        observation_labels_list.append(json.dumps(assignment, ensure_ascii=True, separators=(",", ":")))
        observation_index_rows.append(tuple(outcome_indices))

    independent_masses: list[tuple[Fraction, ...]] = []
    for state_indices in latent_index_rows:
        selected_states = {agent.agent_id: agent.state_labels[index] for agent, index in zip(agents, state_indices, strict=True)}
        selected_components: dict[str, tuple[str, str]] = {}
        for agent_id, state_label in selected_states.items():
            decoded = json.loads(state_label)
            selected_components[agent_id] = (decoded[0], decoded[1])
        generative_mass = Fraction(1)
        for agent in agents:
            if not agent.parent_ids:
                source_label = "()"
            else:
                source_label = json.dumps(
                    [[parent_id, selected_components[parent_id][0], selected_components[parent_id][1]] for parent_id in agent.parent_ids],
                    ensure_ascii=True,
                    separators=(",", ":"),
                )
            source_index = agent.generative_kernel.source_labels.index(source_label)
            target_index = agent.state_labels.index(selected_states[agent.agent_id])
            generative_mass *= agent.generative_kernel.matrix[source_index][target_index]

        independent_row: list[Fraction] = []
        for outcome_indices in observation_index_rows:
            mass = generative_mass
            for record, outcome_index in zip(records, outcome_indices, strict=True):
                source_label = json.dumps(
                    [[agent_id, selected_components[agent_id][0], selected_components[agent_id][1]] for agent_id in record.scope_ids],
                    ensure_ascii=True,
                    separators=(",", ":"),
                )
                source_index = record.kernel.source_labels.index(source_label)
                mass *= record.kernel.matrix[source_index][outcome_index]
            independent_row.append(mass)
        independent_masses.append(tuple(independent_row))

    exact_masses = tuple(independent_masses)
    if sum((sum(row, Fraction(0)) for row in exact_masses), Fraction(0)) != Fraction(1):
        raise ArithmeticError("independently enumerated population joint is not normalized")
    independent_trace = tuple(f"agent:{agent.agent_id}" for agent in agents) + tuple(f"record:{record.record_id}" for record in records)
    return PopulationJoint(
        context_id=context_id,
        agent_order=agent_order,
        record_order=record_ids,
        latent_labels=tuple(latent_labels_list),
        observation_labels=tuple(observation_labels_list),
        joint_masses=exact_masses,
        construction_trace=independent_trace,
    )
