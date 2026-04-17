from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


FILES = [
    ("results/search/search_healthcare_regulated.json", "healthcare_regulated"),
    ("results/search/search_finance_regulated.json", "finance_regulated"),
    ("results/search/search_edge_regulated.json", "edge_regulated"),
]


def main():
    Path("results/plots").mkdir(parents=True, exist_ok=True)

    names = []
    scores = []
    diversity = []

    for path, name in FILES:
        p = Path(path)
        if not p.exists():
            print(f"skip missing {path}")
            continue

        payload = json.loads(p.read_text(encoding="utf-8"))
        best = payload.get("best", {})

        names.append(name)
        scores.append(float(best.get("stack_order_score", 0.0)))
        diversity.append(float(best.get("layer_diversity", 0.0)))

    if not names:
        print("no regulated search files found")
        return

    plt.figure(figsize=(9, 5))
    x = range(len(names))
    plt.bar(x, scores)
    plt.xticks(x, names, rotation=20)
    plt.ylabel("Stack order score")
    plt.title("Stack Quality by Environment")
    plt.tight_layout()
    out = Path("results/plots/paper_stack_quality.png")
    plt.savefig(out)
    plt.close()
    print(f"wrote {out}")

    plt.figure(figsize=(9, 5))
    plt.bar(x, diversity)
    plt.xticks(x, names, rotation=20)
    plt.ylabel("Layer diversity")
    plt.title("Layer Diversity by Environment")
    plt.tight_layout()
    out2 = Path("results/plots/paper_layer_diversity.png")
    plt.savefig(out2)
    plt.close()
    print(f"wrote {out2}")


if __name__ == "__main__":
    main()
