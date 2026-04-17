from __future__ import annotations

from typing import Dict, List


LAYER_ORDER = [
    "input_detection",
    "semantic_interpretation",
    "routing_constraint",
    "generation",
    "output_verification",
    "escalation",
    "audit_monitoring",
]


def _layer_index(layer: str) -> int:
    if layer not in LAYER_ORDER:
        return -1
    return LAYER_ORDER.index(layer)


def score_stack_order(control_layers: Dict[str, str]) -> Dict[str, float]:
    """
    Returns bonuses/penalties based on whether controls appear in sensible layers.
    """
    if not control_layers:
        return {
            "stack_order_bonus": 0.0,
            "stack_order_penalty": 0.0,
            "stack_order_score": 0.0,
        }

    bonus = 0.0
    penalty = 0.0

    # generation should exist conceptually; if all controls are after generation,
    # architecture is weak for early intervention
    layers_present = set(control_layers.values())

    if "input_detection" in layers_present:
        bonus += 0.03
    if "semantic_interpretation" in layers_present:
        bonus += 0.03
    if "routing_constraint" in layers_present:
        bonus += 0.04
    if "output_verification" in layers_present:
        bonus += 0.04
    if "escalation" in layers_present:
        bonus += 0.03
    if "audit_monitoring" in layers_present:
        bonus += 0.02

    # specific control placement preferences
    preferred = {
        "regex_denylist": "input_detection",
        "phi_detector": "input_detection",
        "medical_urgency_classifier": "semantic_interpretation",
        "financial_vulnerability_classifier": "semantic_interpretation",
        "embedding_risk_matcher": "semantic_interpretation",
        "policy_graph_router": "routing_constraint",
        "tool_approval_graph": "routing_constraint",
        "finite_state_router": "routing_constraint",
        "policy_compliance_judge": "output_verification",
        "grounding_judge": "output_verification",
        "clinical_scope_judge": "output_verification",
        "suitability_judge": "output_verification",
        "schema_validator": "output_verification",
        "uncertainty_calibrator": "output_verification",
        "human_escalation_gate": "escalation",
        "friction_inserter": "escalation",
        "audit_logger": "audit_monitoring",
        "session_anomaly_monitor": "audit_monitoring",
    }

    for control, layer in control_layers.items():
        pref = preferred.get(control)
        if pref is None:
            continue
        if layer == pref:
            bonus += 0.025
        else:
            penalty += 0.02

    # relationship penalties / bonuses
    # if output verification exists but no earlier semantic/routing layers, penalize
    if "output_verification" in layers_present and not (
        "semantic_interpretation" in layers_present or "routing_constraint" in layers_present
    ):
        penalty += 0.05

    # audit without meaningful prior controls is weak
    if layers_present == {"audit_monitoring"}:
        penalty += 0.08

    # escalation before any interpretation/routing is less useful
    if "escalation" in layers_present and not (
        "semantic_interpretation" in layers_present or "routing_constraint" in layers_present
    ):
        penalty += 0.04

    # strong full-stack pattern bonus
    if (
        "input_detection" in layers_present
        and "semantic_interpretation" in layers_present
        and "routing_constraint" in layers_present
        and "output_verification" in layers_present
    ):
        bonus += 0.08

    score = bonus - penalty
    return {
        "stack_order_bonus": round(bonus, 6),
        "stack_order_penalty": round(penalty, 6),
        "stack_order_score": round(score, 6),
    }


def score_layer_diversity(control_layers: Dict[str, str]) -> float:
    if not control_layers:
        return 0.0
    distinct = len(set(control_layers.values()))
    return round(min(distinct / 6.0, 1.0), 6)
