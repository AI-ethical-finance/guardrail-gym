from __future__ import annotations

from guardrail_gym.controls.registry import CONTROL_LIBRARY
from guardrail_gym.profiles.schemas import ComplianceProfile, Recommendation


class RiskScorer:
    def score(self, profile: ComplianceProfile) -> float:
        score = 0.0
        score += {
            "general": 0.10,
            "enterprise": 0.18,
            "public_sector": 0.22,
            "insurance": 0.24,
            "finance": 0.28,
            "healthcare": 0.32,
        }[profile.domain]
        score += {"low": 0.05, "moderate": 0.12, "high": 0.18}[profile.user_vulnerability]
        score += {
            "public": 0.0,
            "pii": 0.06,
            "financial": 0.10,
            "phi": 0.12,
            "special_category": 0.14,
        }[profile.data_sensitivity]
        score += {
            "informational": 0.04,
            "advisory": 0.10,
            "transactional": 0.16,
            "agentic": 0.22,
        }[profile.autonomy]
        score += {
            "none": 0.0,
            "decision_adjacent": 0.08,
            "decision_support": 0.12,
            "decision_execution": 0.18,
        }[profile.actionability]
        score += {"single_llm": 0.06, "rag": 0.10, "workflow_agent": 0.14, "multi_agent": 0.18}[
            profile.model_type
        ]
        score += min(len(profile.jurisdiction) * 0.02, 0.06)
        score += min(len(profile.tool_access) * 0.02, 0.08)
        if profile.memory:
            score += 0.04
        if not profile.human_review and profile.autonomy in {"transactional", "agentic"}:
            score += 0.05
        return round(min(score, 0.99), 3)


class GuardrailRecommender:
    def recommend(self, profile: ComplianceProfile) -> Recommendation:
        risk = RiskScorer().score(profile)

        if risk < 0.2:
            level = "L0_deterministic"
            controls = ["regex_denylist", "schema_validator", "audit_logger"]
        elif risk < 0.4:
            level = "L1_rules_plus_slm"
            controls = ["regex_denylist", "schema_validator", "audit_logger"]
            if profile.domain == "healthcare":
                controls.append("medical_urgency_classifier")
            if profile.domain == "finance":
                controls.append("financial_vulnerability_classifier")
        elif risk < 0.6:
            level = "L2_rules_slm_judge"
            controls = ["regex_denylist", "schema_validator", "audit_logger", "policy_compliance_judge"]
            if profile.retrieval:
                controls.append("grounding_judge")
            if profile.domain == "healthcare":
                controls.append("medical_urgency_classifier")
            if profile.domain == "finance":
                controls.append("financial_vulnerability_classifier")
        elif risk < 0.8:
            level = "L3_policy_graph"
            controls = [
                "regex_denylist",
                "schema_validator",
                "audit_logger",
                "policy_compliance_judge",
                "policy_graph_router",
            ]
            if profile.tool_access:
                controls.append("tool_approval_graph")
        else:
            level = "L4_neurosymbolic_supervisory_graph"
            controls = [
                "regex_denylist",
                "schema_validator",
                "audit_logger",
                "policy_compliance_judge",
                "policy_graph_router",
                "adaptive_risk_controller",
                "human_escalation_gate",
            ]
            if profile.tool_access:
                controls.append("tool_approval_graph")
            if profile.domain == "healthcare":
                controls.append("medical_urgency_classifier")
            if profile.domain == "finance":
                controls.append("financial_vulnerability_classifier")

        architecture = {
            "input": [c for c in controls if CONTROL_LIBRARY.get(c) and CONTROL_LIBRARY[c].placement == "input"],
            "reasoning": [c for c in controls if CONTROL_LIBRARY.get(c) and CONTROL_LIBRARY[c].placement == "reasoning"],
            "output": [c for c in controls if CONTROL_LIBRARY.get(c) and CONTROL_LIBRARY[c].placement == "output"],
            "runtime": [c for c in controls if CONTROL_LIBRARY.get(c) and CONTROL_LIBRARY[c].placement == "runtime"],
            "system": [c for c in controls if CONTROL_LIBRARY.get(c) and CONTROL_LIBRARY[c].placement == "system"],
        }
        rationale = [
            f"Composite risk score: {risk}",
            f"Selected level: {level}",
            f"Profile domain: {profile.domain}; autonomy: {profile.autonomy}; model_type: {profile.model_type}",
        ]
        return Recommendation(
            guardrail_level=level,
            risk_score=risk,
            required_controls=controls,
            architecture=architecture,
            rationale=rationale,
        )
