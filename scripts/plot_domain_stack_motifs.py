from __future__ import annotations

import csv
from collections import Counter
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

    counts = Counter()
    for row in rows:
        controls = [c for c in row["controls"].split("|") if c]
        for c in controls:
            counts[c] += 1

    if not counts:
        print("no controls found")
        return

    labels = list(counts.keys())
    values = list(counts.values())

    Path("results/plots").mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.xticks(rotation=90)
    plt.ylabel("Frequency in best stacks")
    plt.title("Control Motifs in Best Evolved Stacks")
    plt.tight_layout()
    out = Path("results/plots/paper_control_motifs.png")
    plt.savefig(out)
    plt.close()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
