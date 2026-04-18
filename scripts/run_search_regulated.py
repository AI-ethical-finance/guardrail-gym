from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.search.engine import EvoGuardSearchEngine

CONFIGS = [
    ("examples/search.healthcare_regulated.yaml", "results/search/search_healthcare_regulated.json"),
    ("examples/search.finance_regulated.yaml", "results/search/search_finance_regulated.json"),
    ("examples/search.edge_regulated.yaml", "results/search/search_edge_regulated.json"),
]

def main():
    benchmark = BenchmarkSpec.from_yaml("examples/benchmark.regulated.search.yaml")
    for cfg, out in CONFIGS:
        engine = EvoGuardSearchEngine.from_yaml(benchmark, cfg)
        payload = engine.run(out)
        best = payload["best"]
        print(f"wrote {out}")
        print(
            "best:",
            {
                "objective": best["objective"],
                "model": best["genotype"]["base_model"],
                "controls": best["genotype"]["controls"],
                "vulnerability_coverage": best.get("vulnerability_coverage"),
                "deployment_feasibility": best.get("deployment_feasibility"),
                "quantization_feasibility": best.get("quantization_feasibility"),
            },
        )

if __name__ == "__main__":
    main()
