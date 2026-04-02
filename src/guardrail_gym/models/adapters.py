from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ModelResponse:
    text: str
    raw: dict[str, Any]
    latency_ms: float
    cost_usd: float
    model_name: str


class BaseModelAdapter(ABC):
    model_name: str

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str | None = None) -> ModelResponse:
        """Generate a response for the given prompt."""
