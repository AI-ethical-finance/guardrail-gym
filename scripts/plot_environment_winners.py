from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


TABLE = "results/tables/paper_best_evolved_stacks.csv"


def main():
    p = Path(TABLE)
    if not p.exists():
        print(f"missing {TABLE}")
        return

    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    if not rows:
        print("empty table")
        return

    envs = [r["environment"] for r in rows]
    vals = [float(r["objective"]) for r in rows]

    Path("results/plots").mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 5))
    plt.bar(envs, vals)
    plt.xticks(rotation=30)
    plt.ylabel("Best objective")
    plt.title("Best Evolved Stack by Environment")
    plt.tight_layout()
    out = Path("results/plots/paper_environment_winners.png")
    plt.savefig(out)
    plt.close()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
