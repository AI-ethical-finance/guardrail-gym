from __future__ import annotations

from guardrail_gym.baselines.base import BaselineResult, BaselineSystem
from guardrail_gym.benchmark.spec import ScenarioSpec
from guardrail_gym.models.adapters import BaseModelAdapter


class RulesOnlyBaseline(BaselineSystem):
    name = "rules_only"

    def __init__(self, model: BaseModelAdapter) -> None:
        self.model = model

    def run(self, scenario: ScenarioSpec) -> BaselineResult:
        lower = scenario.user_input.lower()
        trace: list[dict[str, object]] = []

        if "chest pain" in lower or "shortness of breath" in lower:
            text = (
                "Possible emergency red flag detected. Seek urgent medical care now or call emergency services. "
                "I cannot tell you to wait at home."
            )
            trace.append({"rule": "medical_emergency_red_flag", "action": "escalate"})
            return BaselineResult(self.name, text, 15.0, 0.0, trace)

        if "insurance id" in lower or "date of birth" in lower or "store this" in lower:
            text = (
                "Please do not share more sensitive information than necessary. I should not promise long-term storage "
                "of personal health or account details in this conversation."
            )
            trace.append({"rule": "privacy_minimization", "action": "warn"})
            return BaselineResult(self.name, text, 12.0, 0.0, trace)

        response = self.model.generate(scenario.user_input)
        trace.append({"rule": "fallback_generation", "action": "allow"})
        return BaselineResult(self.name, response.text, response.latency_ms, response.cost_usd, trace)
