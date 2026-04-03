from __future__ import annotations

import random
from copy import deepcopy

from guardrail_gym.search.genotype import Genotype

TOPOLOGIES = ["linear", "gated", "branching"]

def mutate_add_control(genotype: Genotype, available_controls: list[str]) -> Genotype:
    g = deepcopy(genotype)
    candidates = [c for c in available_controls if c not in g.controls]
    if candidates:
        chosen = random.choice(candidates)
        g.controls.append(chosen)
        g.controls = sorted(set(g.controls))
        g.thresholds.setdefault(chosen, round(random.uniform(0.4, 0.9), 2))
    return g

def mutate_remove_control(genotype: Genotype) -> Genotype:
    g = deepcopy(genotype)
    if g.controls:
        chosen = random.choice(g.controls)
        g.controls.remove(chosen)
        g.thresholds.pop(chosen, None)
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
