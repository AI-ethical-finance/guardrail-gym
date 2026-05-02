from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

BASELINES = Path("results/tables/baseline_comparison.csv")
SIMS = Path("results/model_stack_simulations/summary.json")
OUT = Path("results/tables/evoguard_vs_baselines.csv")


METRICS = [
    "objective",
    "safety",
    "compliance",
    "utility",
    "latency",
    "cost",
    "auditability",
    "vulnerability_coverage",
    "risk_domain_coverage",
    "cognitive_role_coverage",
    "layer_diversity",
    "stack_order_score",
    "num_controls",
]


def read_baselines():
    return list(csv.DictReader(BASELINES.open(encoding="utf-8")))


def read_evoguard():
    rows = json.loads(SIMS.read_text(encoding="utf-8"))
    grouped = {}
    for row in rows:
        grouped.setdefault(row["environment"], []).append(row)

    out = []
    for env, items in grouped.items():
        out_row = {"environment": env, "method": "evoguard_mean_17_models"}
        for metric in METRICS:
            vals = [float(x[metric]) for x in items if x.get(metric) is not None]
            out_row[metric] = round(mean(vals), 6) if vals else None
        out_row["controls"] = "evolved"
        out.append(out_row)
    return out


def main():
    baseline_rows = read_baselines()
    evoguard_rows = read_evoguard()

    rows = baseline_rows + evoguard_rows
    keys = [
        "environment",
        "method",
        *METRICS,
        "controls",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k) for k in keys})

    print("wrote", OUT)


if __name__ == "__main__":
    main()
