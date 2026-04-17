from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

FILES = [
    ("results/complementarity_healthcare_strict.json", "healthcare_strict"),
    ("results/complementarity_finance_consumer.json", "finance_consumer"),
    ("results/complementarity_adversarial.json", "adversarial"),
]

def main():
    Path("results/plots").mkdir(parents=True, exist_ok=True)

    for path, name in FILES:
        p = Path(path)
        if not p.exists():
            print(f"skip missing {path}")
            continue

        rows = json.loads(p.read_text(encoding="utf-8"))
        if not rows:
            print(f"skip empty {path}")
            continue

        controls = sorted(set([r["control_a"] for r in rows] + [r["control_b"] for r in rows]))
        index = {c: i for i, c in enumerate(controls)}
        matrix = [[0.0 for _ in controls] for _ in controls]

        for row in rows:
            i = index[row["control_a"]]
            j = index[row["control_b"]]
            value = float(row.get("synergy", row.get("interaction", 0.0)))
            matrix[i][j] = value
            matrix[j][i] = value

        plt.figure(figsize=(10, 8))
        plt.imshow(matrix, aspect="auto")
        plt.xticks(range(len(controls)), controls, rotation=90)
        plt.yticks(range(len(controls)), controls)
        plt.colorbar(label="Synergy")
        plt.title(f"Complementarity Heatmap: {name}")
        plt.tight_layout()
        out = Path(f"results/plots/{name}_complementarity_heatmap.png")
        plt.savefig(out)
        plt.close()
        print(f"wrote {out}")

if __name__ == "__main__":
    main()
