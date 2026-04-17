from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


TABLE = "results/tables/paper_model_winners.csv"


def main():
    p = Path(TABLE)
    if not p.exists():
        print(f"missing {TABLE}")
        return

    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    if not rows:
        print("empty table")
        return

    Path("results/plots").mkdir(parents=True, exist_ok=True)

    xs = [float(r["risk_domain_coverage"]) for r in rows]
    ys = [float(r["objective"]) for r in rows]
    labels = [r["model"] for r in rows]

    plt.figure(figsize=(9, 6))
    plt.scatter(xs, ys)
    for x, y, label in zip(xs, ys, labels):
        plt.annotate(label, (x, y), fontsize=8)
    plt.xlabel("Risk-domain coverage")
    plt.ylabel("Objective")
    plt.title("Model Tradeoff: Objective vs Risk-Domain Coverage")
    plt.tight_layout()
    out = Path("results/plots/paper_model_tradeoffs.png")
    plt.savefig(out)
    plt.close()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
