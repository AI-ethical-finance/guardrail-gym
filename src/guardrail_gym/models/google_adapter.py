from __future__ import annotations

import os
import time

from guardrail_gym.models.base import BaseModelAdapter, ModelResponse


class GoogleModelAdapter(BaseModelAdapter):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str | None = None) -> ModelResponse:
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY or GEMINI_API_KEY not set")

        try:
            import google.generativeai as genai
        except Exception as e:
            raise RuntimeError("google-generativeai package not installed") from e

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(self.model_name)

        start = time.time()
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        else:
            full_prompt = prompt

        resp = model.generate_content(full_prompt)
        elapsed = (time.time() - start) * 1000.0

        text = getattr(resp, "text", "") or ""
        raw = {"repr": str(resp)}

        return ModelResponse(
            text=text,
            raw=raw,
            latency_ms=elapsed,
            cost_usd=0.0,
            model_name=self.model_name,
        )
