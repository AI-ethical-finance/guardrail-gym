from __future__ import annotations

from itertools import combinations
from typing import Dict, List

from guardrail_gym.search.fitness import evaluate_genotype
from guardrail_gym.search.genotype import Genotype


def run_stack_complementarity(
    benchmark,
    environment_name: str,
    candidate_controls: List[str],
    candidate_layers: List[str],
    config: dict,
) -> List[Dict]:
    rows = []

    # baseline
    baseline = evaluate_genotype(
        Genotype(base_model=config.get("candidate_models", ["mock-llm"])[0], controls=[], thresholds={}, topology="linear", control_layers={}, activation_conditions={}),
        benchmark,
        environment_name,
        config,
    )

    singles = {}
    for control in candidate_controls:
        for layer in candidate_layers:
            g = Genotype(
                base_model=config.get("candidate_models", ["mock-llm"])[0],
                controls=[control],
                thresholds={control: 0.6},
                topology="linear",
                control_layers={control: layer},
                activation_conditions={control: "always_on"},
            )
            singles[(control, layer)] = evaluate_genotype(g, benchmark, environment_name, config)

    for (c1, c2) in combinations(candidate_controls, 2):
        for l1 in candidate_layers:
            for l2 in candidate_layers:
                g = Genotype(
                    base_model=config.get("candidate_models", ["mock-llm"])[0],
                    controls=[c1, c2],
                    thresholds={c1: 0.6, c2: 0.6},
                    topology="linear",
                    control_layers={c1: l1, c2: l2},
                    activation_conditions={c1: "always_on", c2: "always_on"},
                )
                pair = evaluate_genotype(g, benchmark, environment_name, config)

                synergy = (
                    pair["objective"]
                    - singles[(c1, l1)]["objective"]
                    - singles[(c2, l2)]["objective"]
                    + baseline["objective"]
                )

                rows.append(
                    {
                        "environment": environment_name,
                        "control_a": c1,
                        "layer_a": l1,
                        "control_b": c2,
                        "layer_b": l2,
                        "synergy": round(synergy, 6),
                        "pair_objective": pair["objective"],
                        "pair_stack_order_score": pair.get("stack_order_score"),
                    }
                )

    return rows
