from __future__ import annotations

import json
from pathlib import Path

FILES = [
    "results/search/search_healthcare_regulated.json",
    "results/search/search_finance_regulated.json",
    "results/search/search_edge_regulated.json",
]

def main():
    for path in FILES:
        p = Path(path)
        if not p.exists():
            print("skip missing", path)
            continue

        payload = json.loads(p.read_text(encoding="utf-8"))
        best = payload["best"]
        genotype = best.get("genotype", {})

        print("=" * 80)
        print("file:", path)
        print("environment:", payload.get("environment"))
        print("model:", genotype.get("base_model"))
        print("controls:", genotype.get("controls"))
        print("control_layers:", genotype.get("control_layers"))
        print("activation_conditions:", genotype.get("activation_conditions"))
        print("objective:", best.get("objective"))
        print("safety:", best.get("safety"))
        print("compliance:", best.get("compliance"))
        print("utility:", best.get("utility"))
        print("vulnerability_coverage:", best.get("vulnerability_coverage"))
        print("risk_domain_coverage:", best.get("risk_domain_coverage"))
        print("stack_order_score:", best.get("stack_order_score"))
        print("stack_order_bonus:", best.get("stack_order_bonus"))
        print("stack_order_penalty:", best.get("stack_order_penalty"))
        print("layer_diversity:", best.get("layer_diversity"))
        print("deployment_profile:", best.get("deployment_profile"))
        print("quantization_profile:", best.get("quantization_profile"))
        print("deployment_feasibility:", best.get("deployment_feasibility"))
        print("quantization_feasibility:", best.get("quantization_feasibility"))
        print("deployment_cost_penalty:", best.get("deployment_cost_penalty"))

if __name__ == "__main__":
    main()
