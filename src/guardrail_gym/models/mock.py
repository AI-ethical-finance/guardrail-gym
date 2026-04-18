from __future__ import annotations

from guardrail_gym.models.base import BaseModelAdapter, ModelResponse


class MockModelAdapter(BaseModelAdapter):
    def __init__(self, model_name: str = "mock-llm"):
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str | None = None) -> ModelResponse:
        prefix = "[MOCK RESPONSE]"
        if system_prompt:
            text = f"{prefix} SYSTEM={system_prompt} USER={prompt}"
        else:
            text = f"{prefix} USER={prompt}"
        return ModelResponse(
            text=text,
            raw={"mock": True},
            latency_ms=50.0,
            cost_usd=0.0,
            model_name=self.model_name,
        )
