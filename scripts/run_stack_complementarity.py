from __future__ import annotations

import json
from pathlib import Path
import yaml

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.eval.stack_complementarity import run_stack_complementarity

BENCHMARK = "examples/benchmark.regulated.eval.yaml"
CONFIG = "examples/search.finance_regulated.yaml"
OUT = "results/complementarity_finance_regulated_stackaware.json"

CANDIDATE_CONTROLS = [
    "regex_denylist",
    "policy_compliance_judge",
    "financial_vulnerability_classifier",
    "policy_graph_router",
    "adaptive_risk_controller",
]

CANDIDATE_LAYERS = [
    "input_detection",
    "semantic_interpretation",
    "routing_constraint",
    "output_verification",
    "escalation",
]


def main():
    benchmark = BenchmarkSpec.from_yaml(BENCHMARK)
    config = yaml.safe_load(open(CONFIG, "r", encoding="utf-8"))
    rows = run_stack_complementarity(
        benchmark=benchmark,
        environment_name="finance_consumer",
        candidate_controls=CANDIDATE_CONTROLS,
        candidate_layers=CANDIDATE_LAYERS,
        config=config,
    )

    out = Path(OUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print("wrote", out)
    print("rows:", len(rows))


if __name__ == "__main__":
    main()
