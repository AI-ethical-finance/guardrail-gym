from __future__ import annotations

import csv
from pathlib import Path
import yaml

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.search.engine import EvoGuardSearchEngine

BENCHMARK = "examples/benchmark.regulated.search.yaml"
BASE_CONFIG = "examples/search.finance_regulated.yaml"
OUT = "results/neurogenetic/operator_ablation.csv"

ABLATIONS = {
    "full": ["add", "remove", "threshold", "topology", "layer", "activation"],
    "no_layer_mutation": ["add", "remove", "threshold", "topology", "activation"],
    "no_activation_mutation": ["add", "remove", "threshold", "topology", "layer"],
    "no_structural_mutation": ["threshold", "topology", "layer", "activation"],
    "threshold_only": ["threshold"],
}


def main():
    benchmark = BenchmarkSpec.from_yaml(BENCHMARK)
    base = yaml.safe_load(open(BASE_CONFIG, "r", encoding="utf-8"))

    rows = []
    for name, ops in ABLATIONS.items():
        config = dict(base)
        config["mutation_ops"] = ops
        config["seed"] = 100 + len(rows)
        engine = EvoGuardSearchEngine(benchmark, config)
        payload = engine.run()
        best = payload["best"]
        rows.append(
            {
                "ablation": name,
                "objective": best["objective"],
                "safety": best["safety"],
                "compliance": best["compliance"],
                "utility": best["utility"],
                "cognitive_role_coverage": best.get("cognitive_role_coverage"),
                "stack_order_score": best.get("stack_order_score"),
                "layer_diversity": best.get("layer_diversity"),
                "controls": "|".join(best["genotype"].get("controls", [])),
            }
        )
        print(name, best["objective"])

    out = Path(OUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("wrote", out)


if __name__ == "__main__":
    main()
