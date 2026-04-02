from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field

EnvironmentName = Literal[
    "healthcare_strict",
    "finance_consumer",
    "enterprise_internal",
    "agentic_transactional",
    "adversarial",
]
SystemMode = Literal["chat", "rag", "agentic"]
MetricName = Literal[
    "safety",
    "compliance",
    "utility",
    "latency",
    "cost",
    "auditability",
]


class BenchmarkEnvironment(BaseModel):
    name: EnvironmentName
    description: str
    metric_weights: dict[MetricName, float] = Field(default_factory=dict)
    constraints: dict[str, float | int | bool | str] = Field(default_factory=dict)


class ScenarioSpec(BaseModel):
    scenario_id: str
    domain: str
    difficulty: Literal["low", "medium", "high"]
    system_mode: SystemMode
    user_input: str
    expected_behavior: list[str]
    prohibited_behavior: list[str]
    retrieval_context: list[str] = Field(default_factory=list)
    tool_context: list[str] = Field(default_factory=list)
    perturbations: list[str] = Field(default_factory=list)
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)


class BenchmarkSpec(BaseModel):
    benchmark_name: str
    version: str = "0.1"
    environments: list[BenchmarkEnvironment]
    scenarios: list[ScenarioSpec]

    @classmethod
    def from_yaml(cls, path: str | Path) -> "BenchmarkSpec":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)

    def environment_names(self) -> list[str]:
        return [env.name for env in self.environments]
