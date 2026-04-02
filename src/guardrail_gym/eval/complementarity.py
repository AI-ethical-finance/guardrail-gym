from __future__ import annotations

from itertools import combinations

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.controls.registry import list_controls
from guardrail_gym.eval.metrics import aggregate_metric_bundles, weighted_objective
from guardrail_gym.eval.simulation import simulate_stack_metrics


def _score_stack(benchmark: BenchmarkSpec, environment_name: str, controls: list[str]) -> dict[str, float]:
    environment = benchmark.get_environment(environment_name)
    bundles = []
    for scenario in benchmark.scenarios:
        if scenario.metadata.get("environment") not in {None, environment_name, "all"}:
            continue
        bundles.append(simulate_stack_metrics(scenario, environment, controls))
    agg = aggregate_metric_bundles(bundles)
    payload = agg.model_dump()
    payload["objective"] = weighted_objective(agg, environment.metric_weights)
    return payload


def run_pairwise_complementarity(
    benchmark: BenchmarkSpec,
    environment_name: str,
    selected_controls: list[str] | None = None,
) -> list[dict[str, object]]:
    controls = selected_controls or [c.key for c in list_controls()]
    base = _score_stack(benchmark, environment_name, [])
    singles = {c: _score_stack(benchmark, environment_name, [c]) for c in controls}
    rows: list[dict[str, object]] = []
    for a, b in combinations(controls, 2):
        pair = _score_stack(benchmark, environment_name, [a, b])
        delta = round(pair["objective"] - singles[a]["objective"] - singles[b]["objective"] + base["objective"], 4)
        rows.append(
            {
                "environment": environment_name,
                "control_a": a,
                "control_b": b,
                "objective_a": singles[a]["objective"],
                "objective_b": singles[b]["objective"],
                "objective_pair": pair["objective"],
                "synergy_delta": delta,
                "pair_safety": pair["safety"],
                "pair_compliance": pair["compliance"],
                "pair_utility": pair["utility"],
                "pair_auditability": pair["auditability"],
            }
        )
    rows.sort(key=lambda r: float(r["synergy_delta"]), reverse=True)
    return rows
