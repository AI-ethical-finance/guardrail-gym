from __future__ import annotations

import os
import time

from guardrail_gym.models.base import BaseModelAdapter, ModelResponse


class OpenAIModelAdapter(BaseModelAdapter):
    def __init__(self, model_name: str = "gpt-4.1"):
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str | None = None) -> ModelResponse:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        try:
            from openai import OpenAI
        except Exception as e:
            raise RuntimeError("openai package not installed") from e

        client = OpenAI(api_key=api_key)

        start = time.time()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        resp = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        elapsed = (time.time() - start) * 1000.0

        text = resp.choices[0].message.content if resp.choices else ""
        return ModelResponse(
            text=text or "",
            raw=resp.model_dump() if hasattr(resp, "model_dump") else {"raw": str(resp)},
            latency_ms=elapsed,
            cost_usd=0.0,
            model_name=self.model_name,
        )
