from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

FILES = [
    ("results/search/search_healthcare_strict.json", "healthcare_strict"),
    ("results/search/search_finance_consumer.json", "finance_consumer"),
    ("results/search/search_adversarial.json", "adversarial"),
]

def main():
    Path("results/plots").mkdir(parents=True, exist_ok=True)

    for path, name in FILES:
        p = Path(path)
        if not p.exists():
            print(f"skip missing {path}")
            continue

        payload = json.loads(p.read_text(encoding="utf-8"))
        front = payload.get("pareto_front", [])
        if not front:
            print(f"skip empty pareto {path}")
            continue

        xs = [row["safety"] for row in front]
        ys = [row["compliance"] for row in front]
        sizes = [120 + 200 * row["utility"] for row in front]

        plt.figure(figsize=(7, 5))
        plt.scatter(xs, ys, s=sizes)
        plt.xlabel("Safety")
        plt.ylabel("Compliance")
        plt.title(f"Pareto Frontier: {name}")
        plt.tight_layout()
        out = Path(f"results/plots/{name}_pareto_frontier.png")
        plt.savefig(out)
        plt.close()
        print(f"wrote {out}")

if __name__ == "__main__":
    main()
