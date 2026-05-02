from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt

SIMS = Path("results/model_stack_simulations/summary.json")
BASELINE_TABLE = Path("results/tables/evoguard_vs_baselines.csv")
OUTDIR = Path("results/plots")


def load_rows():
    return json.loads(SIMS.read_text(encoding="utf-8"))


def plot_group_metric(rows, metric: str, ylabel: str, outfile: str):
    groups = defaultdict(list)
    for r in rows:
        if r.get(metric) is not None:
            groups[r["model_group"]].append(float(r[metric]))

    labels = list(groups.keys())
    vals = [mean(groups[g]) for g in labels]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, vals)
    plt.ylabel(ylabel)
    plt.title(ylabel + " by Model Group")
    plt.xticks(rotation=20)
    plt.tight_layout()
    out = OUTDIR / outfile
    plt.savefig(out)
    plt.close()
    print("wrote", out)


def plot_environment_metric(rows, metric: str, ylabel: str, outfile: str):
    groups = defaultdict(list)
    for r in rows:
        if r.get(metric) is not None:
            groups[r["environment"]].append(float(r[metric]))

    labels = list(groups.keys())
    vals = [mean(groups[g]) for g in labels]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, vals)
    plt.ylabel(ylabel)
    plt.title(ylabel + " by Environment")
    plt.xticks(rotation=20)
    plt.tight_layout()
    out = OUTDIR / outfile
    plt.savefig(out)
    plt.close()
    print("wrote", out)


def plot_baseline_comparison():
    if not BASELINE_TABLE.exists():
        print("skip missing", BASELINE_TABLE)
        return

    rows = list(csv.DictReader(BASELINE_TABLE.open(encoding="utf-8")))
    for env in sorted(set(r["environment"] for r in rows)):
        subset = [r for r in rows if r["environment"] == env]
        labels = [r["method"] for r in subset]
        values = [float(r["objective"]) for r in subset]

        plt.figure(figsize=(10, 5))
        plt.bar(labels, values)
        plt.ylabel("Objective")
        plt.title(f"EvoGuard vs Baselines: {env}")
        plt.xticks(rotation=30)
        plt.tight_layout()
        out = OUTDIR / f"evoguard_vs_baselines_{env}.png"
        plt.savefig(out)
        plt.close()
        print("wrote", out)


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()

    plot_group_metric(rows, "objective", "Mean objective", "model_group_objective.png")
    plot_group_metric(rows, "num_controls", "Mean number of controls", "model_group_stack_size.png")
    plot_group_metric(rows, "latency", "Mean latency", "model_group_latency.png")
    plot_group_metric(rows, "cost", "Mean cost", "model_group_cost.png")

    plot_environment_metric(rows, "layer_diversity", "Mean layer diversity", "environment_layer_diversity.png")
    plot_environment_metric(rows, "auditability", "Mean auditability", "environment_auditability.png")
    plot_environment_metric(rows, "vulnerability_coverage", "Mean vulnerability coverage", "environment_vulnerability_coverage.png")
    plot_environment_metric(rows, "risk_domain_coverage", "Mean risk-domain coverage", "environment_risk_domain_coverage.png")
    plot_environment_metric(rows, "stack_order_score", "Mean stack-order score", "environment_stack_order_score.png")

    plot_baseline_comparison()


if __name__ == "__main__":
    main()
