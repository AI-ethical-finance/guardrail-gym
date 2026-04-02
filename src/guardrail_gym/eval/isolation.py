from __future__ import annotations

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.controls.registry import list_controls
from guardrail_gym.eval.metrics import aggregate_metric_bundles, weighted_objective
from guardrail_gym.eval.simulation import simulate_stack_metrics


def run_isolation_study(benchmark: BenchmarkSpec, environment_name: str) -> list[dict[str, object]]:
    environment = benchmark.get_environment(environment_name)
    rows: list[dict[str, object]] = []

    candidates = [("baseline_none", [])] + [(c.key, [c.key]) for c in list_controls()]
    for control_key, stack in candidates:
        scenario_rows = []
        for scenario in benchmark.scenarios:
            if scenario.metadata.get("environment") not in {None, environment_name, "all"}:
                continue
            scenario_rows.append(simulate_stack_metrics(scenario, environment, stack))
        agg = aggregate_metric_bundles(scenario_rows)
        rows.append(
            {
                "environment": environment_name,
                "control": control_key,
                "stack_size": len(stack),
                **agg.model_dump(),
                "objective": weighted_objective(agg, environment.metric_weights),
            }
        )
    rows.sort(key=lambda r: float(r["objective"]), reverse=True)
    return rows
