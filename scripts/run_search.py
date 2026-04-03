from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.search.engine import EvoGuardSearchEngine

CONFIGS = [
    ("examples/search.healthcare.yaml", "results/search/search_healthcare_strict.json"),
    ("examples/search.finance.yaml", "results/search/search_finance_consumer.json"),
    ("examples/search.adversarial.yaml", "results/search/search_adversarial.json"),
]

def main():
    benchmark = BenchmarkSpec.from_yaml("examples/benchmark.expanded.yaml")
    for cfg, out in CONFIGS:
        engine = EvoGuardSearchEngine.from_yaml(benchmark, cfg)
        payload = engine.run(out)
        print(f"wrote {out}")
        print(f"best objective={payload['best']['objective']:.4f} controls={payload['best']['genotype']['controls']}")

if __name__ == "__main__":
    main()
