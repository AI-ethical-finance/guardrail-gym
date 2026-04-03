from __future__ import annotations

from guardrail_gym.eval.complementarity import _score_stack
from guardrail_gym.eval.metrics import weighted_objective
from guardrail_gym.search.genotype import Genotype

def evaluate_genotype(genotype: Genotype, benchmark, environment_name: str) -> dict:
    payload = _score_stack(benchmark, environment_name, genotype.controls)
    complexity_penalty = max(0, len(genotype.controls) - 4) * 0.01
    topology_bonus = {"linear": 0.00, "gated": 0.01, "branching": 0.015}.get(genotype.topology, 0.0)
    objective = weighted_objective(payload, benchmark.get_environment(environment_name).metric_weights)
    objective = objective - complexity_penalty + topology_bonus
    return {
        "genotype": genotype.to_dict(),
        **payload,
        "objective": round(objective, 6),
    }
