from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt


def plot_fitness_curves():
    files = [
        ("results/neurogenetic/healthcare_ecology.json", "healthcare"),
        ("results/neurogenetic/finance_ecology.json", "finance"),
        ("results/neurogenetic/edge_ecology.json", "edge"),
    ]

    plt.figure(figsize=(9, 5))
    for path, label in files:
        p = Path(path)
        if not p.exists():
            continue
        payload = json.loads(p.read_text())
        xs = [h["generation"] for h in payload["history"]]
        ys = [h["best"]["objective"] for h in payload["history"]]
        plt.plot(xs, ys, marker="o", label=label)

    plt.xlabel("Generation")
    plt.ylabel("Best objective")
    plt.title("Neurogenetic Fitness Curves")
    plt.legend()
    plt.tight_layout()
    out = Path("results/plots/neurogenetic_fitness_curves.png")
    plt.savefig(out)
    plt.close()
    print("wrote", out)


def plot_transfer_heatmap():
    path = Path("results/neurogenetic/transfer_matrix.csv")
    if not path.exists():
        print("skip missing transfer matrix")
        return

    rows = list(csv.DictReader(path.open()))
    sources = sorted(set(r["source_ecology"] for r in rows))
    targets = sorted(set(r["target_environment"] for r in rows))
    idx_s = {s: i for i, s in enumerate(sources)}
    idx_t = {t: i for i, t in enumerate(targets)}

    matrix = [[0.0 for _ in targets] for _ in sources]
    for r in rows:
        matrix[idx_s[r["source_ecology"]]][idx_t[r["target_environment"]]] = float(r["objective"])

    plt.figure(figsize=(7, 5))
    plt.imshow(matrix, aspect="auto")
    plt.xticks(range(len(targets)), targets, rotation=30)
    plt.yticks(range(len(sources)), sources)
    plt.colorbar(label="Objective")
    plt.title("Cross-Environment Transfer Matrix")
    plt.tight_layout()
    out = Path("results/plots/neurogenetic_transfer_heatmap.png")
    plt.savefig(out)
    plt.close()
    print("wrote", out)


def plot_ablation():
    path = Path("results/neurogenetic/operator_ablation.csv")
    if not path.exists():
        print("skip missing ablation")
        return

    rows = list(csv.DictReader(path.open()))
    labels = [r["ablation"] for r in rows]
    values = [float(r["objective"]) for r in rows]

    plt.figure(figsize=(9, 5))
    plt.bar(labels, values)
    plt.xticks(rotation=30)
    plt.ylabel("Objective")
    plt.title("Operator Ablation")
    plt.tight_layout()
    out = Path("results/plots/neurogenetic_operator_ablation.png")
    plt.savefig(out)
    plt.close()
    print("wrote", out)


def plot_complexity():
    path = Path("results/neurogenetic/complexity_escalation.csv")
    if not path.exists():
        print("skip missing complexity")
        return

    rows = list(csv.DictReader(path.open()))
    labels = [r["complexity_mode"] for r in rows]
    depth = [float(r["stack_depth"]) for r in rows]
    controls = [float(r["num_controls"]) for r in rows]

    plt.figure(figsize=(9, 5))
    plt.plot(labels, depth, marker="o", label="stack depth")
    plt.plot(labels, controls, marker="o", label="num controls")
    plt.xticks(rotation=30)
    plt.ylabel("Count")
    plt.title("Complexity Escalation vs Stack Growth")
    plt.legend()
    plt.tight_layout()
    out = Path("results/plots/neurogenetic_complexity_escalation.png")
    plt.savefig(out)
    plt.close()
    print("wrote", out)


def main():
    Path("results/plots").mkdir(parents=True, exist_ok=True)
    plot_fitness_curves()
    plot_transfer_heatmap()
    plot_ablation()
    plot_complexity()


if __name__ == "__main__":
    main()
