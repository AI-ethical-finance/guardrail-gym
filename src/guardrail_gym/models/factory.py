from __future__ import annotations

from guardrail_gym.models.mock import MockModelAdapter
from guardrail_gym.models.openai_adapter import OpenAIModelAdapter


def get_model_adapter(model_name: str):
    if model_name.startswith("gpt-"):
        return OpenAIModelAdapter(model_name=model_name)
    return MockModelAdapter(model_name=model_name)
