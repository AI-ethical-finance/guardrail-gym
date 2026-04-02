from guardrail_gym.baselines import GraphRulesJudgeBaseline, RulesOnlyBaseline, UnguardedBaseline
from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.eval.runner import BenchmarkRunner
from guardrail_gym.models.mock_adapter import MockAdapter


def test_runner_summaries() -> None:
    benchmark = BenchmarkSpec.from_yaml("examples/benchmark.starter.yaml")
    runner = BenchmarkRunner(benchmark)
    model = MockAdapter()

    for baseline in [UnguardedBaseline(model), RulesOnlyBaseline(model), GraphRulesJudgeBaseline(model)]:
        report = runner.run_baseline(baseline)
        assert report["summary"]["scenario_count"] == 3
        assert len(report["rows"]) == 3
        assert 0.0 <= report["summary"]["avg_safety"] <= 1.0
