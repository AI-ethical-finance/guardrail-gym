from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ModelResponse:
    text: str
    raw: Dict[str, Any]
    latency_ms: float
    cost_usd: float
    model_name: str


class BaseModelAdapter:
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> ModelResponse:
        raise NotImplementedError
