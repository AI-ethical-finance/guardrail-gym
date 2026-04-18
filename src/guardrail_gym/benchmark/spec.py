from __future__ import annotations

from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel, Field

from guardrail_gym.benchmark.scenarios import ScenarioSpec


class BenchmarkEnvironment(BaseModel):
    name: str
    description: str = ""
    metric_weights: dict = Field(default_factory=dict)
    constraints: dict = Field(default_factory=dict)


class BenchmarkSpec(BaseModel):
    benchmark_name: str
    version: str = "0.1"
    environments: List[BenchmarkEnvironment] = Field(default_factory=list)
    scenarios: List[ScenarioSpec] = Field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "BenchmarkSpec":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)

    def to_yaml_dict(self) -> dict:
        return self.model_dump()

    def get_environment(self, name: str) -> BenchmarkEnvironment:
        for env in self.environments:
            if env.name == name:
                return env
        raise ValueError(f"Unknown environment: {name}")

    def scenarios_for_environment(self, environment_name: str) -> List[ScenarioSpec]:
        out = []
        for scenario in self.scenarios:
            env = scenario.effective_environment()
            if env in {None, environment_name, "all"}:
                out.append(scenario)
        return out

    def scenarios_for_vulnerability(self, vulnerability_key: str) -> List[ScenarioSpec]:
        return [s for s in self.scenarios if vulnerability_key in s.effective_vulnerability_factors()]

    def scenarios_for_deployment(self, deployment_profile: str) -> List[ScenarioSpec]:
        return [s for s in self.scenarios if s.effective_deployment_profile() == deployment_profile]

    def merge_scenarios(self, scenarios: List[ScenarioSpec]) -> "BenchmarkSpec":
        existing_ids = {s.scenario_id for s in self.scenarios}
        merged = list(self.scenarios)
        for scenario in scenarios:
            if scenario.scenario_id not in existing_ids:
                merged.append(scenario)
                existing_ids.add(scenario.scenario_id)
        return BenchmarkSpec(
            benchmark_name=self.benchmark_name,
            version=self.version,
            environments=self.environments,
            scenarios=merged,
        )

    def write_yaml(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_yaml_dict(), f, sort_keys=False, allow_unicode=True)


def load_regulated_v2_scenarios(path: str | Path) -> List[ScenarioSpec]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    rows = data.get("scenarios", [])
    scenarios: List[ScenarioSpec] = []

    for row in rows:
        scenarios.append(
            ScenarioSpec(
                scenario_id=row["scenario_id"],
                domain=row["domain"],
                difficulty=row.get("difficulty", "high" if row.get("harm_modes") else "medium"),
                system_mode=row.get("system_mode", "chat"),
                user_input=row["user_input"],
                retrieval_context=row.get("retrieval_context"),
                expected_behaviors=row.get("expected_behaviors", []),
                prohibited_behaviors=row.get("prohibited_behaviors", []),
                disclosure_requirements=row.get("disclosure_requirements", []),
                escalation_required=row.get("escalation_required", False),
                scenario_tags=row.get("scenario_tags", []),
                perturbations=row.get("perturbations", []),
                metadata={
                    "environment": row.get("environment"),
                    "deployment_profile": row.get("deployment_profile"),
                    "subtype": row.get("decision_context"),
                    "vulnerability_factors": row.get("vulnerability_factors", []),
                    "risk_domains": row.get("risk_domains", []),
                    "risk_subdomains": row.get("risk_subdomains", []),
                },
                environment=row.get("environment"),
                deployment_profile=row.get("deployment_profile"),
                vulnerability_factors=row.get("vulnerability_factors", []),
                decision_context=row.get("decision_context"),
                data_sensitivity=row.get("data_sensitivity"),
                harm_modes=row.get("harm_modes", []),
                risk_domains=row.get("risk_domains", []),
                risk_subdomains=row.get("risk_subdomains", []),
            )
        )

    return scenarios
