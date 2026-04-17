from __future__ import annotations

import random
from copy import deepcopy

from guardrail_gym.search.control_catalog import control_default_layer
from guardrail_gym.search.genotype import Genotype


TOPOLOGIES = ["linear", "gated", "branching"]
ACTIVATION_MODES = ["always_on", "triggered", "healthcare_only", "finance_only", "rag_only", "agentic_only"]


def mutate_add_control(genotype: Genotype, available_controls: list[str]) -> Genotype:
    g = deepcopy(genotype)
    candidates = [c for c in available_controls if c not in g.controls]
    if candidates:
        chosen = random.choice(candidates)
        g.controls.append(chosen)
        g.controls = sorted(set(g.controls))
        g.thresholds.setdefault(chosen, round(random.uniform(0.4, 0.9), 2))
        g.control_layers.setdefault(chosen, control_default_layer(chosen))
        g.activation_conditions.setdefault(chosen, random.choice(ACTIVATION_MODES))
    return g


def mutate_remove_control(genotype: Genotype) -> Genotype:
    g = deepcopy(genotype)
    if g.controls:
        chosen = random.choice(g.controls)
        g.controls.remove(chosen)
        g.thresholds.pop(chosen, None)
        g.control_layers.pop(chosen, None)
        g.activation_conditions.pop(chosen, None)
    return g


def mutate_threshold(genotype: Genotype) -> Genotype:
    g = deepcopy(genotype)
    if not g.controls:
        return g
    chosen = random.choice(g.controls)
    current = g.thresholds.get(chosen, 0.6)
    delta = random.uniform(-0.15, 0.15)
    g.thresholds[chosen] = round(max(0.0, min(1.0, current + delta)), 2)
    return g


def mutate_topology(genotype: Genotype) -> Genotype:
    g = deepcopy(genotype)
    choices = [t for t in TOPOLOGIES if t != g.topology]
    if choices:
        g.topology = random.choice(choices)
    return g


def mutate_layer(genotype: Genotype) -> Genotype:
    g = deepcopy(genotype)
    if not g.controls:
        return g
    chosen = random.choice(g.controls)
    candidate_layers = [
        "input_detection",
        "semantic_interpretation",
        "routing_constraint",
        "output_verification",
        "escalation",
        "audit_monitoring",
    ]
    g.control_layers[chosen] = random.choice(candidate_layers)
    return g


def mutate_activation(genotype: Genotype) -> Genotype:
    g = deepcopy(genotype)
    if not g.controls:
        return g
    chosen = random.choice(g.controls)
    g.activation_conditions[chosen] = random.choice(ACTIVATION_MODES)
    return g
