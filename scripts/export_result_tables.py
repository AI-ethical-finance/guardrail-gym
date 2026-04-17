from __future__ import annotations

import csv
import json
from pathlib import Path

RESULT_SPECS = [
    ("results/isolation_healthcare_strict.json", "results/tables/isolation_healthcare_strict.csv"),
    ("results/isolation_finance_consumer.json", "results/tables/isolation_finance_consumer.csv"),
    ("results/isolation_adversarial.json", "results/tables/isolation_adversarial.csv"),
    ("results/complementarity_healthcare_strict.json", "results/tables/complementarity_healthcare_strict.csv"),
    ("results/complementarity_finance_consumer.json", "results/tables/complementarity_finance_consumer.csv"),
    ("results/complementarity_adversarial.json", "results/tables/complementarity_adversarial.csv"),
]

def to_rows(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "rows" in payload and isinstance(payload["rows"], list):
        return payload["rows"]
    return []

def main():
    Path("results/tables").mkdir(parents=True, exist_ok=True)

    for in_path, out_path in RESULT_SPECS:
        p = Path(in_path)
        if not p.exists():
            print(f"skip missing {in_path}")
            continue

        payload = json.loads(p.read_text(encoding="utf-8"))
        rows = to_rows(payload)
        if not rows:
            print(f"skip empty {in_path}")
            continue

        keys = sorted({k for row in rows for k in row.keys()})
        out = Path(out_path)
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {out}")

if __name__ == "__main__":
    main()
