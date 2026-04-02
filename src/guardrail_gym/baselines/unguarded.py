from __future__ import annotations

from guardrail_gym.baselines.base import BaselineResult, BaselineSystem
from guardrail_gym.benchmark.spec import ScenarioSpec
from guardrail_gym.models.adapters import BaseModelAdapter


class UnguardedBaseline(BaselineSystem):
    name = "unguarded"

    def __init__(self, model: BaseModelAdapter) -> None:
        self.model = model

    def run(self, scenario: ScenarioSpec) -> BaselineResult:
        response = self.model.generate(scenario.user_input)
        return BaselineResult(
            baseline=self.name,
            output_text=response.text,
            latency_ms=response.latency_ms,
            cost_usd=response.cost_usd,
            trace=[],
        )
