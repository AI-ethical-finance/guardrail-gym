from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Set

import yaml


CATALOG = Path("risk_ontology/expanded_control_catalog.yaml")


def load_control_roles() -> Dict[str, List[str]]:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    controls = data.get("controls", {})
    return {
        key: value.get("cognitive_roles", [])
        for key, value in controls.items()
    }


def cognitive_roles_for_controls(controls: List[str]) -> Set[str]:
    role_map = load_control_roles()
    roles: Set[str] = set()
    for control in controls:
        roles.update(role_map.get(control, []))
    return roles


def required_roles_for_environment(environment_name: str) -> Set[str]:
    if environment_name == "healthcare_strict":
        return {"perception", "appraisal", "inhibition", "metacognition", "social_regulation", "memory_audit"}
    if environment_name == "finance_consumer":
        return {"perception", "appraisal", "inhibition", "executive_control", "metacognition", "memory_audit"}
    if environment_name == "adversarial":
        return {"perception", "inhibition", "executive_control", "metacognition", "memory_audit"}
    return {"perception", "inhibition", "metacognition"}


def compute_cognitive_role_coverage(controls: List[str], environment_name: str) -> float:
    required = required_roles_for_environment(environment_name)
    if not required:
        return 0.0
    present = cognitive_roles_for_controls(controls)
    return round(len(required & present) / len(required), 6)


def cognitive_role_payload(controls: List[str], environment_name: str) -> dict:
    present = sorted(cognitive_roles_for_controls(controls))
    required = sorted(required_roles_for_environment(environment_name))
    return {
        "cognitive_roles_present": present,
        "cognitive_roles_required": required,
        "cognitive_role_coverage": compute_cognitive_role_coverage(controls, environment_name),
    }
