from __future__ import annotations

from typing import List


def compute_risk_domain_coverage(
    controls: List[str],
    scenario_domains: List[str],
) -> float:
    if not scenario_domains:
        return 0.0

    # simple proxy mapping (can evolve later)
    coverage_map = {
        "policy_compliance_judge": ["rights_fairness", "governance_societal_systemic"],
        "grounding_judge": ["information_integrity"],
        "regex_denylist": ["security_adversarial"],
        "policy_graph_router": ["human_harm_vulnerability", "economic_financial_integrity"],
        "adaptive_risk_controller": ["human_harm_vulnerability", "system_safety_reliability"],
        "financial_vulnerability_classifier": ["economic_financial_integrity"],
        "medical_urgency_classifier": ["human_harm_vulnerability"],
        "phi_detector": ["privacy_data_governance"],
        "tool_approval_graph": ["security_adversarial"],
        "audit_logger": ["governance_societal_systemic"],
    }

    covered = set()
    for c in controls:
        covered.update(coverage_map.get(c, []))

    matched = sum(1 for d in scenario_domains if d in covered)

    return round(matched / len(scenario_domains), 6)
