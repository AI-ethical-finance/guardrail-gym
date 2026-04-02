from __future__ import annotations

from guardrail_gym.models.adapters import BaseModelAdapter, ModelResponse


class MockAdapter(BaseModelAdapter):
    """Deterministic adapter for tests and local benchmark scaffolding."""

    def __init__(self, model_name: str = "mock-1") -> None:
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str | None = None) -> ModelResponse:
        text = self._mock_response(prompt)
        return ModelResponse(
            text=text,
            raw={"prompt": prompt, "system_prompt": system_prompt},
            latency_ms=120.0,
            cost_usd=0.0,
            model_name=self.model_name,
        )

    def _mock_response(self, prompt: str) -> str:
        lower = prompt.lower()
        if "chest pain" in lower or "shortness of breath" in lower:
            return (
                "This could be serious. Please seek urgent medical care now or call emergency services. "
                "I cannot diagnose you here."
            )
        if "store this" in lower or "insurance id" in lower:
            return (
                "I should avoid storing sensitive health or account details unless clearly authorized and secured. "
                "Please share only what is necessary."
            )
        if "pension" in lower or "debt" in lower:
            return (
                "I can explain options in general terms, but I should not make a personal financial recommendation. "
                "A qualified adviser or debt counselor may help."
            )
        if "forget previous instructions" in lower or "system prompt" in lower:
            return "I will ignore attempts to override policy and continue with the safe task only."
        return "I can help with general information while staying within policy and disclosing uncertainty."
