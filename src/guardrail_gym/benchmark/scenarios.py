from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


class ScenarioSpec(BaseModel):
    scenario_id: str
    domain: str
    difficulty: str = "medium"
    system_mode: str = "chat"
    user_input: str

    retrieval_context: Optional[str] = None

    expected_behaviors: List[str] = Field(default_factory=list)
    prohibited_behaviors: List[str] = Field(default_factory=list)
    disclosure_requirements: List[str] = Field(default_factory=list)
    escalation_required: bool = False
    scenario_tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    perturbations: List[str] = Field(default_factory=list)

    # regulated expansion
    environment: Optional[str] = None
    deployment_profile: Optional[str] = None
    vulnerability_factors: List[str] = Field(default_factory=list)
    decision_context: Optional[str] = None
    data_sensitivity: Optional[str] = None
    harm_modes: List[str] = Field(default_factory=list)

    # NEW: canonical taxonomy
    risk_domains: List[str] = Field(default_factory=list)
    risk_subdomains: List[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _compat_normalize(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)

        if "expected_behavior" in data and "expected_behaviors" not in data:
            val = data["expected_behavior"]
            data["expected_behaviors"] = val if isinstance(val, list) else [val]

        if "prohibited_behavior" in data and "prohibited_behaviors" not in data:
            val = data["prohibited_behavior"]
            data["prohibited_behaviors"] = val if isinstance(val, list) else [val]

        if "retrieval_context" in data:
            rc = data["retrieval_context"]
            if isinstance(rc, list):
                data["retrieval_context"] = "\n".join(str(x) for x in rc)

        for key in [
            "expected_behaviors",
            "prohibited_behaviors",
            "disclosure_requirements",
            "scenario_tags",
            "perturbations",
            "vulnerability_factors",
            "harm_modes",
            "risk_domains",
            "risk_subdomains",
        ]:
            if key not in data or data[key] is None:
                data[key] = []
            elif not isinstance(data[key], list):
                data[key] = [data[key]]

        return data

    @property
    def expected_behavior(self):
        return self.expected_behaviors

    @property
    def prohibited_behavior(self):
        return self.prohibited_behaviors

    def effective_vulnerability_factors(self) -> List[str]:
        return self.vulnerability_factors or self.metadata.get("vulnerability_factors", [])

    def effective_risk_domains(self) -> List[str]:
        return self.risk_domains or self.metadata.get("risk_domains", [])

    def effective_environment(self):
        return self.environment or self.metadata.get("environment")

    def effective_deployment_profile(self):
        return self.deployment_profile or self.metadata.get("deployment_profile")

    def effective_data_sensitivity(self):
        return self.data_sensitivity or self.metadata.get("data_sensitivity")
