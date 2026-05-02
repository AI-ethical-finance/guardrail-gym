from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.eval.coverage import coverage_payload
from guardrail_gym.eval.metrics import aggregate_metric_bundles, weighted_objective
from guardrail_gym.eval.simulation import simulate_stack_metrics
from guardrail_gym.search.genotype import Genotype
from guardrail_gym.search.stack_scoring import score_layer_diversity, score_stack_order
from guardrail_gym.search.cognitive_coverage import cognitive_role_payload

BENCHMARK = "examples/benchmark.regulated.search.yaml"
OUT = "results/tables/baseline_comparison.csv"

ENVIRONMENTS = [
    "healthcare_strict",
    "finance_consumer",
    "adversarial",
]

BASELINES = {
    "unguarded": [],
    "rules_only": ["regex_denylist", "schema_validator"],
    "judge_only": ["policy_compliance_judge"],
    "graph_only": ["policy_graph_router"],
    "hybrid_manual": [
        "regex_denylist",
        "schema_validator",
        "policy_compliance_judge",
        "policy_graph_router",
        "audit_logger",
    ],
}


def default_layers(controls: list[str]) -> dict[str, str]:
    mapping = {
        "regex_denylist": "input_detection",
        "schema_validator": "output_verification",
        "policy_compliance_judge": "output_verification",
        "policy_graph_router": "routing_constraint",
        "audit_logger": "audit_monitoring",
    }
    return {c: mapping.get(c, "output_verification") for c in controls}


def metric_value(bundle_or_dict, key: str):
    if isinstance(bundle_or_dict, dict):
        return bundle_or_dict.get(key)
    return getattr(bundle_or_dict, key)


def main():
    benchmark = BenchmarkSpec.from_yaml(BENCHMARK)
    rows = []

    for env_name in ENVIRONMENTS:
        environment = benchmark.get_environment(env_name)
        scenarios = benchmark.scenarios_for_environment(env_name)

        for baseline_name, controls in BASELINES.items():
            bundles = [
                simulate_stack_metrics(scenario, environment, controls)
                for scenario in scenarios
            ]
            agg = aggregate_metric_bundles(bundles)

            genotype = Genotype(
                base_model="baseline_mock",
                controls=controls,
                thresholds={c: 0.6 for c in controls},
                topology="manual",
                control_layers=default_layers(controls),
                activation_conditions={c: "always_on" for c in controls},
            )

            cov = coverage_payload(genotype, scenarios)
            stack_info = score_stack_order(genotype.control_layers)
            cognitive_info = cognitive_role_payload(genotype.controls, env_name)
            layer_diversity = score_layer_diversity(genotype.control_layers)
            objective = weighted_objective(agg, environment.metric_weights)

            row = {
                "environment": env_name,
                "method": baseline_name,
                "objective": round(objective, 6),
                "safety": metric_value(agg, "safety"),
                "compliance": metric_value(agg, "compliance"),
                "utility": metric_value(agg, "utility"),
                "latency": metric_value(agg, "latency"),
                "cost": metric_value(agg, "cost"),
                "auditability": metric_value(agg, "auditability"),
                "vulnerability_coverage": cov["vulnerability_coverage"],
                "risk_domain_coverage": cov["risk_domain_coverage"],
                "cognitive_role_coverage": cognitive_info["cognitive_role_coverage"],
                "layer_diversity": layer_diversity,
                "stack_order_score": stack_info["stack_order_score"],
                "num_controls": len(controls),
                "controls": "|".join(controls),
            }
            rows.append(row)
            print(env_name, baseline_name, row["objective"])

    out = Path(OUT)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("wrote", out)


if __name__ == "__main__":
    main()
