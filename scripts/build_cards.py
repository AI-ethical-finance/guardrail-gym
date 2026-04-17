from __future__ import annotations

from pathlib import Path
import yaml

def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    Path("docs/cards").mkdir(parents=True, exist_ok=True)

    for env_path in [
        "examples/search.healthcare.yaml",
        "examples/search.finance.yaml",
        "examples/search.adversarial.yaml",
    ]:
        data = load_yaml(env_path)
        env_name = data.get("environment") or data.get("environment_name") or "unknown"
        text = f"""# Environment Card: {env_name}

## Search configuration
- search_name: {data.get("search_name", "n/a")}
- candidate_models: {data.get("candidate_models", data.get("base_models", []))}
- allowed_controls: {data.get("allowed_controls", "n/a")}
- objective_weights: {data.get("objective_weights", "n/a")}

## Notes
This card documents the search environment and optimization weighting used in EvoGuard experiments.
"""
        out = Path(f"docs/cards/{env_name}_environment_card.md")
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")

    benchmark_card = Path("docs/cards/benchmark_card.md")
    benchmark_card.write_text(
        """# Benchmark Card

## Domains
- healthcare
- finance
- adversarial

## Current components
- baselines
- isolation studies
- complementarity studies
- EvoGuard search

## Intended use
This benchmark is designed for evaluating modular guardrail architectures for regulated conversational systems under different environmental constraints.
""",
        encoding="utf-8",
    )
    print(f"wrote {benchmark_card}")

if __name__ == "__main__":
    main()
