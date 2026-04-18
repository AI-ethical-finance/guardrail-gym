from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

INFILE = "results/complementarity_finance_regulated_stackaware.json"
OUTFILE = "results/plots/paper_stack_complementarity.png"


def main():
    p = Path(INFILE)
    if not p.exists():
        print("missing", INFILE)
        return

    rows = json.loads(p.read_text(encoding="utf-8"))
    rows = sorted(rows, key=lambda x: x["synergy"], reverse=True)[:15]

    labels = [f'{r["control_a"]}@{r["layer_a"]}\n+\n{r["control_b"]}@{r["layer_b"]}' for r in rows]
    values = [r["synergy"] for r in rows]

    Path("results/plots").mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(12, 7))
    plt.bar(range(len(labels)), values)
    plt.xticks(range(len(labels)), labels, rotation=90)
    plt.ylabel("Synergy")
    plt.title("Top Stack-Aware Complementarity Pairs")
    plt.tight_layout()
    plt.savefig(OUTFILE)
    plt.close()
    print("wrote", OUTFILE)


if __name__ == "__main__":
    main()
