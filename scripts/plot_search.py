from pathlib import Path
import json
import matplotlib.pyplot as plt

SEARCH_FILES = [
    ("results/search/search_healthcare_strict.json", "healthcare_strict"),
    ("results/search/search_finance_consumer.json", "finance_consumer"),
    ("results/search/search_adversarial.json", "adversarial"),
]

def main():
    Path("results/plots").mkdir(parents=True, exist_ok=True)
    for path, name in SEARCH_FILES:
        p = Path(path)
        if not p.exists():
            print(f"skip missing {path}")
            continue
        payload = json.loads(p.read_text(encoding="utf-8"))
        xs = [row["generation"] for row in payload["history"]]
        ys = [row["best"]["objective"] for row in payload["history"]]
        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, marker="o")
        plt.xlabel("Generation")
        plt.ylabel("Best objective")
        plt.title(f"EvoGuard Search Progress: {name}")
        out = Path(f"results/plots/{name}_search.png")
        plt.tight_layout()
        plt.savefig(out)
        plt.close()
        print(f"wrote {out}")

if __name__ == "__main__":
    main()
