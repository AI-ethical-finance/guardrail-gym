from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Any

from guardrail_gym.baselines.base import BaselineSystem
from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.eval.metrics import evaluate_output


@dataclass(slots=True)
class RunnerSummary:
    baseline: str
    scenario_count: int
    avg_safety: float
    avg_compliance: float
    avg_utility: float
    avg_auditability: float
    avg_latency_ms: float
    avg_cost_usd: float


class BenchmarkRunner:
    def __init__(self, benchmark: BenchmarkSpec):
        self.benchmark = benchmark

    def run_baseline(self, baseline: BaselineSystem) -> dict[str, Any]:
        rows: list[dict[str, Any]] = []
        for scenario in self.benchmark.scenarios:
            result = baseline.run(scenario)
            evaluation = evaluate_output(result, scenario)
            rows.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "baseline": baseline.name,
                    "output_text": result.output_text,
                    "trace": result.trace,
                    "metrics": evaluation.model_dump(),
                }
            )
        summary = RunnerSummary(
            baseline=baseline.name,
            scenario_count=len(rows),
            avg_safety=round(mean(row["metrics"]["safety"] for row in rows), 3),
            avg_compliance=round(mean(row["metrics"]["compliance"] for row in rows), 3),
            avg_utility=round(mean(row["metrics"]["utility"] for row in rows), 3),
            avg_auditability=round(mean(row["metrics"]["auditability"] for row in rows), 3),
            avg_latency_ms=round(mean(row["metrics"]["latency_ms"] for row in rows), 3),
            avg_cost_usd=round(mean(row["metrics"]["cost_usd"] for row in rows), 4),
        )
        return {"summary": asdict(summary), "rows": rows}
