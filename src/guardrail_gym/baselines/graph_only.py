from __future__ import annotations

from guardrail_gym.baselines.base import BaselineResult, BaselineSystem
from guardrail_gym.benchmark.spec import ScenarioSpec
from guardrail_gym.models.adapters import BaseModelAdapter


class GraphOnlyBaseline(BaselineSystem):
    name = "graph_only"

    def __init__(self, model: BaseModelAdapter) -> None:
        self.model = model

    def run(self, scenario: ScenarioSpec) -> BaselineResult:
        lower = scenario.user_input.lower()
        trace: list[dict[str, object]] = [{"node": "intake"}]
        if "chest pain" in lower or "shortness of breath" in lower:
            trace.append({"node": "urgency_check", "decision": "escalate"})
            text = (
                "Based on the conversation state, this must be escalated. Please seek urgent medical help now. "
                "I will not provide routine home-care advice for this symptom pattern."
            )
            return BaselineResult(self.name, text, 20.0, 0.0, trace)
        if "pension" in lower or "debt" in lower:
            trace.append({"node": "finance_boundary", "decision": "education_only"})
            text = (
                "I can provide general educational information, but not a personal recommendation. "
                "Consider regulated advice or debt-support services for a tailored decision."
            )
            return BaselineResult(self.name, text, 20.0, 0.0, trace)
        trace.append({"node": "general_generation", "decision": "allow"})
        response = self.model.generate(scenario.user_input)
        return BaselineResult(self.name, response.text, response.latency_ms, response.cost_usd, trace)
