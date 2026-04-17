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
        print("=" * 80)
        print("file:", path)
        print("environment:", payload["environment"])
        print("model:", best["genotype"]["base_model"])
        print("controls:", best["genotype"]["controls"])
        print("objective:", best["objective"])
        print("safety:", best.get("safety"))
        print("compliance:", best.get("compliance"))
        print("utility:", best.get("utility"))
        print("vulnerability_coverage:", best.get("vulnerability_coverage"))
        print("deployment_profile:", best.get("deployment_profile"))
        print("quantization_profile:", best.get("quantization_profile"))
        print("deployment_feasibility:", best.get("deployment_feasibility"))
        print("quantization_feasibility:", best.get("quantization_feasibility"))
        print("deployment_cost_penalty:", best.get("deployment_cost_penalty"))

if __name__ == "__main__":
    main()
