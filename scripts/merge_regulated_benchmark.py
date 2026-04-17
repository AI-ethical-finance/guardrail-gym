from guardrail_gym.benchmark.spec import BenchmarkSpec, load_regulated_v2_scenarios

BASE_BENCHMARK = "examples/benchmark.expanded.yaml"
REGULATED_SCENARIOS = "benchmark_data/regulated_v2/sample_regulated_scenarios.yaml"
OUT_PATH = "examples/benchmark.regulated.yaml"

def main():
    base = BenchmarkSpec.from_yaml(BASE_BENCHMARK)
    regulated = load_regulated_v2_scenarios(REGULATED_SCENARIOS)
    merged = base.merge_scenarios(regulated)
    merged.write_yaml(OUT_PATH)

    print(f"base scenarios: {len(base.scenarios)}")
    print(f"regulated scenarios added: {len(regulated)}")
    print(f"merged scenarios: {len(merged.scenarios)}")
    print(f"wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
