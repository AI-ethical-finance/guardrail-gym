from __future__ import annotations

import json
from pathlib import Path

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.search.engine import EvoGuardSearchEngine

EXPERIMENTS = [
    {
        "name": "healthcare_ecology",
        "config": "examples/search.healthcare_regulated.yaml",
        "output": "results/neurogenetic/healthcare_ecology.json",
    },
    {
        "name": "finance_ecology",
        "config": "examples/search.finance_regulated.yaml",
        "output": "results/neurogenetic/finance_ecology.json",
    },
    {
        "name": "edge_ecology",
        "config": "examples/search.edge_regulated.yaml",
        "output": "results/neurogenetic/edge_ecology.json",
    },
]

BENCHMARK = "examples/benchmark.regulated.search.yaml"


def summarize_run(payload: dict) -> dict:
    best = payload["best"]
    genotype = best["genotype"]
    return {
        "environment": payload["environment"],
        "model": genotype.get("base_model"),
        "controls": genotype.get("controls", []),
        "control_layers": genotype.get("control_layers", {}),
        "objective": best.get("objective"),
        "safety": best.get("safety"),
        "compliance": best.get("compliance"),
        "utility": best.get("utility"),
        "vulnerability_coverage": best.get("vulnerability_coverage"),
        "risk_domain_coverage": best.get("risk_domain_coverage"),
        "cognitive_role_coverage": best.get("cognitive_role_coverage"),
        "cognitive_roles_present": best.get("cognitive_roles_present"),
        "stack_order_score": best.get("stack_order_score"),
        "layer_diversity": best.get("layer_diversity"),
    }


def main():
    benchmark = BenchmarkSpec.from_yaml(BENCHMARK)
    summaries = []

    for exp in EXPERIMENTS:
        engine = EvoGuardSearchEngine.from_yaml(benchmark, exp["config"])
        payload = engine.run(exp["output"])
        summary = summarize_run(payload)
        summary["experiment"] = exp["name"]
        summaries.append(summary)
        print("=" * 80)
        print(exp["name"])
        print(summary)

    out = Path("results/neurogenetic/summary.json")
    out.write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
