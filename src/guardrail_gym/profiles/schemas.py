from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ComplianceProfile(BaseModel):
    domain: Literal["healthcare", "finance", "insurance", "public_sector", "enterprise", "general"]
    jurisdiction: list[str]
    user_vulnerability: Literal["low", "moderate", "high"]
    data_sensitivity: Literal["public", "pii", "financial", "phi", "special_category"]
    autonomy: Literal["informational", "advisory", "transactional", "agentic"]
    actionability: Literal["none", "decision_adjacent", "decision_support", "decision_execution"]
    model_type: Literal["single_llm", "rag", "workflow_agent", "multi_agent"]
    retrieval: bool = False
    memory: bool = False
    human_review: bool = False
    tool_access: list[str] = Field(default_factory=list)


class Recommendation(BaseModel):
    guardrail_level: str
    risk_score: float
    required_controls: list[str]
    architecture: dict[str, list[str]]
    rationale: list[str]
