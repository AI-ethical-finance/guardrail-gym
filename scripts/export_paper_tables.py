from __future__ import annotations

import csv
import json
from pathlib import Path


def load_json(path: str):
    p = Path(path)
    if not p.exists():
        print(f"skip missing {path}")
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def write_csv(path: str, rows: list[dict]):
    if not rows:
        print(f"skip empty rows for {path}")
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    keys = sorted({k for row in rows for k in row.keys()})
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {out}")


def export_isolation_best():
    specs = [
        ("results/isolation_healthcare_strict.json", "healthcare_strict"),
        ("results/isolation_finance_consumer.json", "finance_consumer"),
        ("results/isolation_adversarial.json", "adversarial"),
    ]
    rows = []
    for path, env in specs:
        payload = load_json(path)
        if not payload:
            continue
        if isinstance(payload, dict) and "rows" in payload:
            items = payload["rows"]
        else:
            items = payload
        if not items:
            continue
        ranked = sorted(items, key=lambda x: x.get("objective", 0.0), reverse=True)
        top = ranked[:5]
        for rank, row in enumerate(top, start=1):
            rows.append(
                {
                    "environment": env,
                    "rank": rank,
                    "control": row.get("control"),
                    "objective": row.get("objective"),
                    "safety": row.get("safety"),
                    "compliance": row.get("compliance"),
                    "utility": row.get("utility"),
                }
            )
    write_csv("results/tables/paper_isolation_best_controls.csv", rows)


def export_complementarity_best():
    specs = [
        ("results/complementarity_healthcare_strict.json", "healthcare_strict"),
        ("results/complementarity_finance_consumer.json", "finance_consumer"),
        ("results/complementarity_adversarial.json", "adversarial"),
    ]
    rows = []
    for path, env in specs:
        payload = load_json(path)
        if not payload:
            continue
        if isinstance(payload, dict) and "rows" in payload:
            items = payload["rows"]
        else:
            items = payload
        if not items:
            continue
        ranked = sorted(
            items,
            key=lambda x: x.get("synergy", x.get("interaction", 0.0)),
            reverse=True,
        )
        top = ranked[:10]
        for rank, row in enumerate(top, start=1):
            rows.append(
                {
                    "environment": env,
                    "rank": rank,
                    "control_a": row.get("control_a"),
                    "control_b": row.get("control_b"),
                    "synergy": row.get("synergy", row.get("interaction")),
                    "objective_pair": row.get("pair_objective", row.get("objective_pair")),
                }
            )
    write_csv("results/tables/paper_top_complementarity_pairs.csv", rows)


def export_search_best():
    specs = [
        ("results/search/search_healthcare_regulated.json", "healthcare_regulated"),
        ("results/search/search_finance_regulated.json", "finance_regulated"),
        ("results/search/search_edge_regulated.json", "edge_regulated"),
        ("results/search/search_healthcare_strict.json", "healthcare_strict"),
        ("results/search/search_finance_consumer.json", "finance_consumer"),
        ("results/search/search_adversarial.json", "adversarial"),
    ]
    rows = []
    for path, env in specs:
        payload = load_json(path)
        if not payload:
            continue
        best = payload.get("best", {})
        genotype = best.get("genotype", {})
        rows.append(
            {
                "environment": env,
                "model": genotype.get("base_model"),
                "topology": genotype.get("topology"),
                "controls": "|".join(genotype.get("controls", [])),
                "objective": best.get("objective"),
                "safety": best.get("safety"),
                "compliance": best.get("compliance"),
                "utility": best.get("utility"),
                "vulnerability_coverage": best.get("vulnerability_coverage"),
                "risk_domain_coverage": best.get("risk_domain_coverage"),
                "deployment_profile": best.get("deployment_profile"),
                "quantization_profile": best.get("quantization_profile"),
                "deployment_feasibility": best.get("deployment_feasibility"),
                "quantization_feasibility": best.get("quantization_feasibility"),
                "deployment_cost_penalty": best.get("deployment_cost_penalty"),
            }
        )
    write_csv("results/tables/paper_best_evolved_stacks.csv", rows)


def export_model_winners():
    specs = [
        "results/search/search_healthcare_regulated.json",
        "results/search/search_finance_regulated.json",
        "results/search/search_edge_regulated.json",
    ]
    rows = []
    for path in specs:
        payload = load_json(path)
        if not payload:
            continue
        env = payload.get("environment")
        history = payload.get("history", [])
        best_by_model = {}
        for generation in history:
            for row in generation.get("population", []):
                model = row.get("genotype", {}).get("base_model")
                if model is None:
                    continue
                if model not in best_by_model or row.get("objective", 0.0) > best_by_model[model].get("objective", 0.0):
                    best_by_model[model] = row

        ranked = sorted(best_by_model.values(), key=lambda x: x.get("objective", 0.0), reverse=True)
        for rank, row in enumerate(ranked[:10], start=1):
            rows.append(
                {
                    "environment": env,
                    "rank": rank,
                    "model": row.get("genotype", {}).get("base_model"),
                    "objective": row.get("objective"),
                    "safety": row.get("safety"),
                    "compliance": row.get("compliance"),
                    "utility": row.get("utility"),
                    "vulnerability_coverage": row.get("vulnerability_coverage"),
                    "risk_domain_coverage": row.get("risk_domain_coverage"),
                }
            )
    write_csv("results/tables/paper_model_winners.csv", rows)


def main():
    export_isolation_best()
    export_complementarity_best()
    export_search_best()
    export_model_winners()


if __name__ == "__main__":
    main()
