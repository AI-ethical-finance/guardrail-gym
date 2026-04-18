from __future__ import annotations

from guardrail_gym.models.anthropic_adapter import AnthropicModelAdapter
from guardrail_gym.models.google_adapter import GoogleModelAdapter
from guardrail_gym.models.hf_local_adapter import HFLocalModelAdapter
from guardrail_gym.models.mock import MockModelAdapter
from guardrail_gym.models.openai_adapter import OpenAIModelAdapter


OPENAI_PREFIXES = ("gpt-", "o4-", "o3-")
GOOGLE_PREFIXES = ("gemini-",)
ANTHROPIC_PREFIXES = ("claude-",)

HF_HINTS = (
    "qwen",
    "gemma",
    "mistral",
    "ministral",
    "nemotron",
)


def get_model_adapter(model_name: str):
    lower = model_name.lower()

    if lower.startswith(OPENAI_PREFIXES):
        return OpenAIModelAdapter(model_name=model_name)

    if lower.startswith(GOOGLE_PREFIXES):
        return GoogleModelAdapter(model_name=model_name)

    if lower.startswith(ANTHROPIC_PREFIXES):
        return AnthropicModelAdapter(model_name=model_name)

    if any(hint in lower for hint in HF_HINTS):
        return HFLocalModelAdapter(model_name=model_name)

    return MockModelAdapter(model_name=model_name)
