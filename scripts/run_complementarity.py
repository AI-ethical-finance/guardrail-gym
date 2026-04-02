from __future__ import annotations

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.controls.registry import list_controls
from guardrail_gym.eval.complementarity import run_pairwise_complementarity
from guardrail_gym.eval.reports import write_csv, write_json


def main() -> None:
    spec = BenchmarkSpec.from_yaml("examples/benchmark.expanded.yaml")
    selected = [
        "regex_denylist",
        "schema_validator",
        "medical_urgency_classifier",
        "financial_vulnerability_classifier",
        "policy_compliance_judge",
        "policy_graph_router",
        "adaptive_risk_controller",
        "human_escalation_gate",
    ]
    for env in ["healthcare_strict", "finance_consumer", "adversarial"]:
        rows = run_pairwise_complementarity(spec, env, selected_controls=selected)
        write_json(f"results/complementarity_{env}.json", rows)
        write_csv(f"results/complementarity_{env}.csv", rows)
        print(f"wrote results/complementarity_{env}.json")


if __name__ == "__main__":
    main()
