from __future__ import annotations

import csv
import json
from pathlib import Path

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.search.fitness import evaluate_genotype
from guardrail_gym.search.genotype import Genotype

BENCHMARK = "examples/benchmark.regulated.eval.yaml"

SOURCES = [
    ("healthcare_ecology", "results/neurogenetic/healthcare_ecology.json"),
    ("finance_ecology", "results/neurogenetic/finance_ecology.json"),
    ("edge_ecology", "results/neurogenetic/edge_ecology.json"),
]

TARGET_ENVIRONMENTS = [
    "healthcare_strict",
    "finance_consumer",
    "adversarial",
]

OUT = "results/neurogenetic/transfer_matrix.csv"


def main():
    benchmark = BenchmarkSpec.from_yaml(BENCHMARK)
    rows = []

    for source_name, path in SOURCES:
        p = Path(path)
        if not p.exists():
            print("skip missing", path)
            continue

        payload = json.loads(p.read_text(encoding="utf-8"))
        genotype = Genotype(**payload["best"]["genotype"])
        config = payload.get("config", {})

        for target_env in TARGET_ENVIRONMENTS:
            scored = evaluate_genotype(genotype, benchmark, target_env, config)
            rows.append(
                {
                    "source_ecology": source_name,
                    "target_environment": target_env,
                    "objective": scored["objective"],
                    "safety": scored["safety"],
                    "compliance": scored["compliance"],
                    "utility": scored["utility"],
                    "vulnerability_coverage": scored["vulnerability_coverage"],
                    "risk_domain_coverage": scored["risk_domain_coverage"],
                    "cognitive_role_coverage": scored.get("cognitive_role_coverage"),
                    "stack_order_score": scored["stack_order_score"],
                }
            )

    out = Path(OUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    keys = rows[0].keys() if rows else []
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)

    print("wrote", out)


if __name__ == "__main__":
    main()
