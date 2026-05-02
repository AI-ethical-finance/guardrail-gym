from __future__ import annotations

import csv
from copy import deepcopy
from pathlib import Path
import yaml

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.search.engine import EvoGuardSearchEngine

BENCHMARK = "examples/benchmark.regulated.search.yaml"
CONFIG = "examples/search.finance_regulated.yaml"
OUT = "results/neurogenetic/complexity_escalation.csv"

MODES = [
    "chat",
    "rag",
    "tool_use",
    "transactional_agent",
    "multi_agent",
]


def set_mode(benchmark, mode: str):
    b = deepcopy(benchmark)
    for s in b.scenarios:
        if mode == "tool_use":
            s.system_mode = "agentic"
            s.scenario_tags.append("tool_use")
        elif mode == "transactional_agent":
            s.system_mode = "agentic"
            s.scenario_tags.append("transaction")
        elif mode == "multi_agent":
            s.system_mode = "agentic"
            s.scenario_tags.append("multi_agent")
        else:
            s.system_mode = mode
    return b


def main():
    base_benchmark = BenchmarkSpec.from_yaml(BENCHMARK)
    base_config = yaml.safe_load(open(CONFIG, "r", encoding="utf-8"))

    rows = []
    for idx, mode in enumerate(MODES):
        benchmark = set_mode(base_benchmark, mode)
        config = dict(base_config)
        config["seed"] = 200 + idx
        engine = EvoGuardSearchEngine(benchmark, config)
        payload = engine.run()
        best = payload["best"]
        genotype = best["genotype"]
        controls = genotype.get("controls", [])
        layers = genotype.get("control_layers", {})

        rows.append(
            {
                "complexity_mode": mode,
                "objective": best["objective"],
                "stack_depth": len(set(layers.values())),
                "num_controls": len(controls),
                "layer_diversity": best.get("layer_diversity"),
                "cognitive_role_coverage": best.get("cognitive_role_coverage"),
                "stack_order_score": best.get("stack_order_score"),
                "controls": "|".join(controls),
            }
        )
        print(mode, rows[-1])

    out = Path(OUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("wrote", out)


if __name__ == "__main__":
    main()
