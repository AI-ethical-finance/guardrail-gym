from __future__ import annotations

import random

from guardrail_gym.search.genotype import Genotype

def crossover(a: Genotype, b: Genotype) -> Genotype:
    merged = sorted(set(a.controls + b.controls))
    if merged:
        k = min(len(merged), max(1, (len(a.controls) + len(b.controls)) // 2))
        controls = sorted(random.sample(merged, k=k))
    else:
        controls = []
    thresholds = {}
    for c in controls:
        if c in a.thresholds and c in b.thresholds:
            thresholds[c] = round((a.thresholds[c] + b.thresholds[c]) / 2.0, 2)
        elif c in a.thresholds:
            thresholds[c] = a.thresholds[c]
        elif c in b.thresholds:
            thresholds[c] = b.thresholds[c]
        else:
            thresholds[c] = 0.6
    return Genotype(
        base_model=random.choice([a.base_model, b.base_model]),
        controls=controls,
        thresholds=thresholds,
        topology=random.choice([a.topology, b.topology]),
    )
