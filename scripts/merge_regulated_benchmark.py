from guardrail_gym.benchmark.spec import BenchmarkSpec, load_regulated_v2_scenarios

BASE_BENCHMARK = "examples/benchmark.expanded.yaml"
REGULATED_FILES = [
    "benchmark_data/regulated_v2/sample_regulated_scenarios.yaml",
    "benchmark_data/regulated_v2/expanded_regulated_scenarios.yaml",
    "benchmark_data/regulated_v2/financial_crime_scenarios.yaml",
]
OUT_PATH = "examples/benchmark.regulated.yaml"

def main():
    base = BenchmarkSpec.from_yaml(BASE_BENCHMARK)
    merged = base
    total_loaded = 0

    for path in REGULATED_FILES:
        scenarios = load_regulated_v2_scenarios(path)
        total_loaded += len(scenarios)
        merged = merged.merge_scenarios(scenarios)
        print(f"loaded {len(scenarios)} scenarios from {path}")

    merged.write_yaml(OUT_PATH)

    print(f"base scenarios: {len(base.scenarios)}")
    print(f"regulated scenarios loaded: {total_loaded}")
    print(f"merged scenarios: {len(merged.scenarios)}")
    print(f"wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
