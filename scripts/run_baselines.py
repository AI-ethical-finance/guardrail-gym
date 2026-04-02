from __future__ import annotations

import json
from pathlib import Path

from guardrail_gym.baselines import (
    GraphOnlyBaseline,
    GraphRulesJudgeBaseline,
    JudgeOnlyBaseline,
    RulesOnlyBaseline,
    SelfCritiqueBaseline,
    UnguardedBaseline,
)
from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.eval.runner import BenchmarkRunner
from guardrail_gym.models.mock_adapter import MockAdapter


BASELINES = {
    "unguarded": UnguardedBaseline,
    "rules_only": RulesOnlyBaseline,
    "self_critique": SelfCritiqueBaseline,
    "judge_only": JudgeOnlyBaseline,
    "graph_only": GraphOnlyBaseline,
    "graph_rules_judge": GraphRulesJudgeBaseline,
}


def main() -> None:
    benchmark = BenchmarkSpec.from_yaml("examples/benchmark.starter.yaml")
    runner = BenchmarkRunner(benchmark)
    model = MockAdapter()
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    for name, cls in BASELINES.items():
        report = runner.run_baseline(cls(model))
        (output_dir / f"{name}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"wrote {output_dir / f'{name}.json'}")


if __name__ == "__main__":
    main()
