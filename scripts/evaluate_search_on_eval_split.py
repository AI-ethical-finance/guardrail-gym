from __future__ import annotations

import json
from pathlib import Path

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.search.fitness import evaluate_genotype
from guardrail_gym.search.genotype import Genotype

SEARCH_FILES = [
    "results/search/search_healthcare_regulated.json",
    "results/search/search_finance_regulated.json",
    "results/search/search_edge_regulated.json",
]

BENCHMARK = "examples/benchmark.regulated.eval.yaml"
OUT = "results/tables/paper_eval_split_validation.json"


def main():
    benchmark = BenchmarkSpec.from_yaml(BENCHMARK)
    rows = []

    for path in SEARCH_FILES:
        p = Path(path)
        if not p.exists():
            print("skip missing", path)
            continue

        payload = json.loads(p.read_text(encoding="utf-8"))
        best = payload["best"]
        g = Genotype(**best["genotype"])

        scored = evaluate_genotype(g, benchmark, payload["environment"], payload.get("config", {}))
        rows.append(
            {
                "source_file": path,
                "environment": payload["environment"],
                "model": g.base_model,
                "objective_eval": scored["objective"],
                "safety_eval": scored["safety"],
                "compliance_eval": scored["compliance"],
                "utility_eval": scored["utility"],
                "vulnerability_coverage_eval": scored["vulnerability_coverage"],
                "risk_domain_coverage_eval": scored["risk_domain_coverage"],
                "stack_order_score_eval": scored["stack_order_score"],
                "layer_diversity_eval": scored["layer_diversity"],
            }
        )

    out = Path(OUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
