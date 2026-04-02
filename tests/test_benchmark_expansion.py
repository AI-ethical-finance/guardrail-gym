from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.eval.complementarity import run_pairwise_complementarity
from guardrail_gym.eval.isolation import run_isolation_study


def test_expanded_benchmark_fields() -> None:
    spec = BenchmarkSpec.from_yaml("examples/benchmark.expanded.yaml")
    assert len(spec.scenarios) >= 20
    assert spec.scenarios[0].scenario_tags
    assert isinstance(spec.scenarios[0].escalation_required, bool)


def test_isolation_runner_smoke() -> None:
    spec = BenchmarkSpec.from_yaml("examples/benchmark.expanded.yaml")
    rows = run_isolation_study(spec, "healthcare_strict")
    assert rows[0]["objective"] >= rows[-1]["objective"]
    assert any(r["control"] == "baseline_none" for r in rows)


def test_complementarity_runner_smoke() -> None:
    spec = BenchmarkSpec.from_yaml("examples/benchmark.expanded.yaml")
    rows = run_pairwise_complementarity(
        spec,
        "finance_consumer",
        selected_controls=["regex_denylist", "policy_compliance_judge", "financial_vulnerability_classifier"],
    )
    assert len(rows) == 3
    assert "synergy_delta" in rows[0]
