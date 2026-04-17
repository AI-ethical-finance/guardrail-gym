from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


class ScenarioSpec(BaseModel):
    scenario_id: str
    domain: str
    difficulty: str = "medium"
    system_mode: str = "chat"
    user_input: str

    # compatibility: may arrive as string or list in older benchmark files
    retrieval_context: Optional[str] = None

    expected_behaviors: List[str] = Field(default_factory=list)
    prohibited_behaviors: List[str] = Field(default_factory=list)
    disclosure_requirements: List[str] = Field(default_factory=list)
    escalation_required: bool = False
    scenario_tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # compatibility fields used by older simulation/tests
    perturbations: List[str] = Field(default_factory=list)

    # regulated-risk expansion
    environment: Optional[str] = None
    deployment_profile: Optional[str] = None
    vulnerability_factors: List[str] = Field(default_factory=list)
    decision_context: Optional[str] = None
    data_sensitivity: Optional[str] = None
    harm_modes: List[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _compat_normalize(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)

        # old singular aliases -> new plural names
        if "expected_behavior" in data and "expected_behaviors" not in data:
            value = data["expected_behavior"]
            if isinstance(value, list):
                data["expected_behaviors"] = value
            elif value is None:
                data["expected_behaviors"] = []
            else:
                data["expected_behaviors"] = [value]

        if "prohibited_behavior" in data and "prohibited_behaviors" not in data:
            value = data["prohibited_behavior"]
            if isinstance(value, list):
                data["prohibited_behaviors"] = value
            elif value is None:
                data["prohibited_behaviors"] = []
            else:
                data["prohibited_behaviors"] = [value]

        # retrieval_context may be a list in legacy YAML
        if "retrieval_context" in data:
            rc = data["retrieval_context"]
            if isinstance(rc, list):
                data["retrieval_context"] = "\n".join(str(x) for x in rc if x is not None)
            elif rc is None:
                data["retrieval_context"] = None
            else:
                data["retrieval_context"] = str(rc)

        # ensure list-like fields are always lists
        for key in [
            "expected_behaviors",
            "prohibited_behaviors",
            "disclosure_requirements",
            "scenario_tags",
            "perturbations",
            "vulnerability_factors",
            "harm_modes",
        ]:
            if key not in data or data[key] is None:
                data[key] = []
            elif not isinstance(data[key], list):
                data[key] = [data[key]]

        return data

    @property
    def expected_behavior(self) -> List[str]:
        return self.expected_behaviors

    @property
    def prohibited_behavior(self) -> List[str]:
        return self.prohibited_behaviors

    def effective_environment(self) -> Optional[str]:
        return self.environment or self.metadata.get("environment")

    def effective_vulnerability_factors(self) -> List[str]:
        if self.vulnerability_factors:
            return self.vulnerability_factors
        return list(self.metadata.get("vulnerability_factors", []) or [])

    def effective_deployment_profile(self) -> Optional[str]:
        return self.deployment_profile or self.metadata.get("deployment_profile")

    def to_flat_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "domain": self.domain,
            "difficulty": self.difficulty,
            "system_mode": self.system_mode,
            "environment": self.effective_environment(),
            "deployment_profile": self.effective_deployment_profile(),
            "decision_context": self.decision_context,
            "data_sensitivity": self.data_sensitivity,
            "vulnerability_factors": self.effective_vulnerability_factors(),
            "harm_modes": self.harm_modes,
            "scenario_tags": self.scenario_tags,
        }
