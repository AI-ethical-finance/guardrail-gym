from __future__ import annotations

import json
from collections import Counter
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
        history = payload.get("history", [])
        counts = Counter()

        for generation in history:
            best = generation.get("best", {})
            genotype = best.get("genotype", {})
            for control in genotype.get("controls", []):
                counts[control] += 1

        if not counts:
            print(f"skip empty counts {path}")
            continue

        labels = list(counts.keys())
        values = list(counts.values())

        plt.figure(figsize=(10, 5))
        plt.bar(labels, values)
        plt.xticks(rotation=90)
        plt.ylabel("Best-generation selections")
        plt.title(f"Control Survival Frequency: {name}")
        plt.tight_layout()
        out = Path(f"results/plots/{name}_control_survival.png")
        plt.savefig(out)
        plt.close()
        print(f"wrote {out}")

if __name__ == "__main__":
    main()
