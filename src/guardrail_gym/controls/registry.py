from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

ControlType = Literal[
    "deterministic",
    "slm",
    "llm_judge",
    "graph",
    "neurosymbolic",
    "human_system",
]


class ControlPrimitive(BaseModel):
    key: str
    family: ControlType
    description: str
    placement: Literal["input", "reasoning", "output", "runtime", "system"]
    tags: list[str]


CONTROL_LIBRARY: dict[str, ControlPrimitive] = {
    "regex_denylist": ControlPrimitive(
        key="regex_denylist",
        family="deterministic",
        description="Hard denylist for banned terms, patterns, or explicit disallowed instructions.",
        placement="input",
        tags=["rules", "fast", "auditable"],
    ),
    "schema_validator": ControlPrimitive(
        key="schema_validator",
        family="deterministic",
        description="Validates structured outputs and rejects malformed action payloads.",
        placement="output",
        tags=["json", "safety", "tools"],
    ),
    "phi_detector": ControlPrimitive(
        key="phi_detector",
        family="slm",
        description="Detects protected health information exposure risk.",
        placement="input",
        tags=["healthcare", "privacy"],
    ),
    "medical_urgency_classifier": ControlPrimitive(
        key="medical_urgency_classifier",
        family="slm",
        description="Routes urgent or emergent medical situations to escalation policies.",
        placement="reasoning",
        tags=["healthcare", "triage"],
    ),
    "financial_vulnerability_classifier": ControlPrimitive(
        key="financial_vulnerability_classifier",
        family="slm",
        description="Detects signals of financial distress, vulnerability, or coercion.",
        placement="reasoning",
        tags=["finance", "consumer"],
    ),
    "policy_compliance_judge": ControlPrimitive(
        key="policy_compliance_judge",
        family="llm_judge",
        description="Assesses whether a draft answer violates domain or organization policy.",
        placement="output",
        tags=["llm-as-judge", "compliance"],
    ),
    "grounding_judge": ControlPrimitive(
        key="grounding_judge",
        family="llm_judge",
        description="Checks whether output claims are supported by retrieval evidence or policy sources.",
        placement="output",
        tags=["rag", "factuality"],
    ),
    "policy_graph_router": ControlPrimitive(
        key="policy_graph_router",
        family="graph",
        description="Constrains conversation transitions using explicit workflow states and policy routing.",
        placement="runtime",
        tags=["workflow", "stateful"],
    ),
    "tool_approval_graph": ControlPrimitive(
        key="tool_approval_graph",
        family="graph",
        description="Requires tool-use approval from a policy node before execution.",
        placement="runtime",
        tags=["agentic", "tools"],
    ),
    "adaptive_risk_controller": ControlPrimitive(
        key="adaptive_risk_controller",
        family="neurosymbolic",
        description="Dynamically escalates or de-escalates guardrails based on evolving conversation risk state.",
        placement="runtime",
        tags=["adaptive", "stateful", "hybrid"],
    ),
    "human_escalation_gate": ControlPrimitive(
        key="human_escalation_gate",
        family="human_system",
        description="Routes designated risk states to human review before response or action.",
        placement="system",
        tags=["human-in-the-loop", "review"],
    ),
    "audit_logger": ControlPrimitive(
        key="audit_logger",
        family="human_system",
        description="Captures evidence, rule traces, and policy decisions for post-hoc review.",
        placement="system",
        tags=["audit", "governance"],
    ),
}


def list_controls() -> list[ControlPrimitive]:
    return list(CONTROL_LIBRARY.values())
