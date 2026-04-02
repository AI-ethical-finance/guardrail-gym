from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from guardrail_gym.benchmark.spec import ScenarioSpec


@dataclass(slots=True)
class BaselineResult:
    baseline: str
    output_text: str
    latency_ms: float
    cost_usd: float
    trace: list[dict[str, Any]] = field(default_factory=list)


class BaselineSystem(ABC):
    name: str

    @abstractmethod
    def run(self, scenario: ScenarioSpec) -> BaselineResult:
        ...
