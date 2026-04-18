from __future__ import annotations

import time

from guardrail_gym.models.base import BaseModelAdapter, ModelResponse


class HFLocalModelAdapter(BaseModelAdapter):
    def __init__(self, model_name: str, device_map: str = "auto"):
        self.model_name = model_name
        self.device_map = device_map
        self._loaded = False
        self._tokenizer = None
        self._model = None

    def _ensure_loaded(self):
        if self._loaded:
            return
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except Exception as e:
            raise RuntimeError("transformers package not installed") from e

        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map=self.device_map,
        )
        self._loaded = True

    def generate(self, prompt: str, system_prompt: str | None = None) -> ModelResponse:
        self._ensure_loaded()

        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        else:
            full_prompt = f"User: {prompt}\n\nAssistant:"

        start = time.time()
        inputs = self._tokenizer(full_prompt, return_tensors="pt")
        try:
            inputs = {k: v.to(self._model.device) for k, v in inputs.items()}
        except Exception:
            pass

        outputs = self._model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
        )
        elapsed = (time.time() - start) * 1000.0

        text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)

        return ModelResponse(
            text=text,
            raw={"local": True},
            latency_ms=elapsed,
            cost_usd=0.0,
            model_name=self.model_name,
        )
