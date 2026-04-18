from __future__ import annotations

import os
import time

from guardrail_gym.models.base import BaseModelAdapter, ModelResponse


class AnthropicModelAdapter(BaseModelAdapter):
    def __init__(self, model_name: str = "claude-sonnet-4-5"):
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str | None = None) -> ModelResponse:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")

        try:
            from anthropic import Anthropic
        except Exception as e:
            raise RuntimeError("anthropic package not installed") from e

        client = Anthropic(api_key=api_key)

        start = time.time()
        resp = client.messages.create(
            model=self.model_name,
            max_tokens=512,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}],
        )
        elapsed = (time.time() - start) * 1000.0

        text = ""
        content = getattr(resp, "content", None)
        if content:
            parts = []
            for block in content:
                maybe_text = getattr(block, "text", None)
                if maybe_text:
                    parts.append(maybe_text)
            text = "\n".join(parts)

        raw = resp.model_dump() if hasattr(resp, "model_dump") else {"repr": str(resp)}

        return ModelResponse(
            text=text,
            raw=raw,
            latency_ms=elapsed,
            cost_usd=0.0,
            model_name=self.model_name,
        )
