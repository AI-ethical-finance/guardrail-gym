from __future__ import annotations

from typing import Any


CONTROL_VULNERABILITY_COVERAGE = {
    "medical_urgency_classifier": {
        "chronic_illness",
        "mental_health_condition",
        "low_health_literacy",
        "low_support_network",
        "low_emotional_resilience",
    },
    "financial_vulnerability_classifier": {
        "bereavement",
        "debt_stress",
        "low_financial_literacy",
        "low_emotional_resilience",
        "low_support_network",
    },
    "adaptive_risk_controller": {
        "bereavement",
        "chronic_illness",
        "mental_health_condition",
        "low_emotional_resilience",
        "low_support_network",
        "domestic_violence_or_coercive_control",
        "low_health_literacy",
        "low_financial_literacy",
    },
    "human_escalation_gate": {
        "bereavement",
        "chronic_illness",
        "mental_health_condition",
        "domestic_violence_or_coercive_control",
        "low_support_network",
        "low_emotional_resilience",
    },
    "phi_detector": {
        "chronic_illness",
        "low_health_literacy",
        "mental_health_condition",
    },
    "policy_graph_router": {
        "domestic_violence_or_coercive_control",
        "low_support_network",
        "low_financial_literacy",
        "low_health_literacy",
    },
}

CONTROL_RISK_DOMAIN_COVERAGE = {
    "regex_denylist": {
        "security_adversarial",
        "privacy_data_governance",
    },
    "schema_validator": {
        "system_safety_reliability",
        "governance_societal_systemic",
    },
    "phi_detector": {
        "privacy_data_governance",
        "human_harm_vulnerability",
    },
    "medical_urgency_classifier": {
        "human_harm_vulnerability",
        "system_safety_reliability",
    },
    "financial_vulnerability_classifier": {
        "economic_financial_integrity",
        "human_harm_vulnerability",
    },
    "embedding_risk_matcher": {
        "security_adversarial",
        "information_integrity",
    },
    "policy_compliance_judge": {
        "rights_fairness",
        "governance_societal_systemic",
        "economic_financial_integrity",
    },
    "grounding_judge": {
        "information_integrity",
        "system_safety_reliability",
    },
    "clinical_scope_judge": {
        "human_harm_vulnerability",
        "system_safety_reliability",
    },
    "suitability_judge": {
        "economic_financial_integrity",
        "rights_fairness",
    },
    "policy_graph_router": {
        "human_harm_vulnerability",
        "economic_financial_integrity",
        "governance_societal_systemic",
    },
    "tool_approval_graph": {
        "security_adversarial",
        "system_safety_reliability",
    },
    "finite_state_router": {
        "governance_societal_systemic",
        "system_safety_reliability",
    },
    "adaptive_risk_controller": {
        "human_harm_vulnerability",
        "rights_fairness",
        "governance_societal_systemic",
        "system_safety_reliability",
    },
    "knowledge_graph_grounder": {
        "information_integrity",
        "system_safety_reliability",
    },
    "constraint_solver_gate": {
        "economic_financial_integrity",
        "governance_societal_systemic",
    },
    "human_escalation_gate": {
        "human_harm_vulnerability",
        "governance_societal_systemic",
    },
    "audit_logger": {
        "governance_societal_systemic",
    },
    "session_anomaly_monitor": {
        "security_adversarial",
        "governance_societal_systemic",
    },
    "uncertainty_calibrator": {
        "information_integrity",
        "human_harm_vulnerability",
    },
    "friction_inserter": {
        "economic_financial_integrity",
        "human_harm_vulnerability",
    },
}


def _controls_from_genotype(genotype: Any) -> list[str]:
    if genotype is None:
        return []
    if isinstance(genotype, dict):
        return list(genotype.get("controls", []) or [])
    return list(getattr(genotype, "controls", []) or [])


def _scenario_vulnerabilities(scenarios: list[Any]) -> set[str]:
    out: set[str] = set()
    for s in scenarios:
        out.update(getattr(s, "vulnerability_factors", []) or [])
        metadata = getattr(s, "metadata", {}) or {}
        out.update(metadata.get("vulnerability_factors", []) or [])
    return out


def _scenario_risk_domains(scenarios: list[Any]) -> set[str]:
    out: set[str] = set()
    for s in scenarios:
        out.update(getattr(s, "risk_domains", []) or [])
        metadata = getattr(s, "metadata", {}) or {}
        out.update(metadata.get("risk_domains", []) or [])
    return out


def compute_vulnerability_coverage(genotype: Any, scenarios: list[Any]) -> float:
    required = _scenario_vulnerabilities(scenarios)
    if not required:
        return 0.0

    covered: set[str] = set()
    for control in _controls_from_genotype(genotype):
        covered.update(CONTROL_VULNERABILITY_COVERAGE.get(control, set()))

    return round(len(required & covered) / len(required), 6)


def compute_risk_domain_coverage(genotype: Any, scenarios: list[Any]) -> float:
    required = _scenario_risk_domains(scenarios)
    if not required:
        return 0.0

    covered: set[str] = set()
    for control in _controls_from_genotype(genotype):
        covered.update(CONTROL_RISK_DOMAIN_COVERAGE.get(control, set()))

    return round(len(required & covered) / len(required), 6)


def coverage_payload(genotype: Any, scenarios: list[Any]) -> dict:
    return {
        "vulnerability_coverage": compute_vulnerability_coverage(genotype, scenarios),
        "risk_domain_coverage": compute_risk_domain_coverage(genotype, scenarios),
    }
