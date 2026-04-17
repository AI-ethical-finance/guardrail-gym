from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml


def _load_yaml(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def load_control_coverage() -> dict:
    data = _load_yaml("risk_ontology/control_coverage_matrix.yaml")
    return data["controls"]


def compute_vulnerability_coverage(controls: List[str], vulnerability_factors: List[str]) -> float:
    if not vulnerability_factors:
        return 0.0

    coverage_map = load_control_coverage()
    total = 0.0

    for vf in vulnerability_factors:
        best = 0.0
        for control in controls:
            ctrl = coverage_map.get(control, {})
            covers = ctrl.get("covers", {})
            best = max(best, float(covers.get(vf, 0.0)))
        total += best

    return round(total / max(len(vulnerability_factors), 1), 6)


def deployment_penalty(model_record: Dict, deployment_profile: str, quantization_profile: str) -> Dict[str, float]:
    supported = set(model_record.get("deployment_modes", []))
    precisions = set(model_record.get("precision_profiles", []))

    deploy_ok = 1.0 if deployment_profile in supported else 0.0
    quant_ok = 1.0 if quantization_profile in precisions else 0.0

    cost_penalty = {
        "low": 0.05,
        "medium": 0.12,
        "high": 0.25,
        "very_low": 0.02,
    }.get(model_record.get("cost_tier", "medium"), 0.12)

    if deploy_ok == 0.0:
        cost_penalty += 0.25
    if quant_ok == 0.0:
        cost_penalty += 0.15

    return {
        "deployment_feasibility": deploy_ok,
        "quantization_feasibility": quant_ok,
        "deployment_cost_penalty": round(cost_penalty, 6),
    }
