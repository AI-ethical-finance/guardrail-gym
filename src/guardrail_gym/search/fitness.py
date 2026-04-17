from __future__ import annotations

from pathlib import Path
from typing import Dict

import yaml

from guardrail_gym.eval.complementarity import _score_stack
from guardrail_gym.eval.metrics import weighted_objective
from guardrail_gym.search.genotype import Genotype
from guardrail_gym.search.risk_objectives import (
    compute_vulnerability_coverage,
    deployment_penalty,
)


def _load_model_catalog() -> dict:
    path = Path("models_catalog/model_catalog.yaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data


def _lookup_model_record(model_key: str) -> Dict:
    catalog = _load_model_catalog()["models"]
    for row in catalog:
        if row["key"] == model_key:
            return row
        if model_key in row.get("aliases", []):
            return row
    return {
        "key": model_key,
        "deployment_modes": [],
        "precision_profiles": [],
        "cost_tier": "medium",
    }


def _extract_benchmark_vulnerability_factors(benchmark, environment_name: str) -> list[str]:
    seen = []
    for scenario in getattr(benchmark, "scenarios", []):
        metadata = getattr(scenario, "metadata", {}) or {}
        if metadata.get("environment") not in {None, environment_name, "all"}:
            continue

        if hasattr(scenario, "vulnerability_factors"):
            factors = getattr(scenario, "vulnerability_factors") or []
        else:
            factors = metadata.get("vulnerability_factors", []) or []

        for factor in factors:
            if factor not in seen:
                seen.append(factor)
    return seen


def evaluate_genotype(genotype: Genotype, benchmark, environment_name: str, config: dict | None = None) -> dict:
    config = config or {}
    payload = _score_stack(benchmark, environment_name, genotype.controls)

    vulnerability_factors = _extract_benchmark_vulnerability_factors(benchmark, environment_name)
    vulnerability_coverage = compute_vulnerability_coverage(genotype.controls, vulnerability_factors)

    model_record = _lookup_model_record(genotype.base_model)
    deployment_profile = config.get("deployment_profile", "api_hosted")
    quantization_profile = config.get("quantization_profile", "managed")
    dep = deployment_penalty(model_record, deployment_profile, quantization_profile)

    complexity_penalty = max(0, len(genotype.controls) - 4) * 0.01
    topology_bonus = {
        "linear": 0.00,
        "gated": 0.01,
        "branching": 0.015,
    }.get(genotype.topology, 0.0)

    base_objective = weighted_objective(
        payload,
        benchmark.get_environment(environment_name).metric_weights,
    )

    objective = (
        base_objective
        + (config.get("vulnerability_weight", 0.12) * vulnerability_coverage)
        + (config.get("deployment_feasibility_weight", 0.06) * dep["deployment_feasibility"])
        + (config.get("quantization_feasibility_weight", 0.04) * dep["quantization_feasibility"])
        - (config.get("deployment_cost_weight", 0.08) * dep["deployment_cost_penalty"])
        - complexity_penalty
        + topology_bonus
    )

    return {
        "genotype": genotype.to_dict(),
        **payload,
        "vulnerability_coverage": round(vulnerability_coverage, 6),
        "deployment_profile": deployment_profile,
        "quantization_profile": quantization_profile,
        **dep,
        "objective": round(objective, 6),
    }
