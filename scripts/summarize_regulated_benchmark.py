from collections import Counter

from guardrail_gym.benchmark.spec import BenchmarkSpec

BENCHMARK = "examples/benchmark.regulated.yaml"

def main():
    benchmark = BenchmarkSpec.from_yaml(BENCHMARK)

    env_counts = Counter()
    vuln_counts = Counter()
    deploy_counts = Counter()
    domain_counts = Counter()
    sensitivity_counts = Counter()

    for scenario in benchmark.scenarios:
        domain_counts[scenario.domain] += 1
        if scenario.effective_environment():
            env_counts[scenario.effective_environment()] += 1
        if scenario.effective_deployment_profile():
            deploy_counts[scenario.effective_deployment_profile()] += 1
        if scenario.data_sensitivity:
            sensitivity_counts[scenario.data_sensitivity] += 1
        for vf in scenario.effective_vulnerability_factors():
            vuln_counts[vf] += 1

    print("benchmark:", benchmark.benchmark_name)
    print("version:", benchmark.version)
    print("total scenarios:", len(benchmark.scenarios))
    print("\nby domain:")
    for k, v in domain_counts.most_common():
        print(f"  {k}: {v}")

    print("\nby environment:")
    for k, v in env_counts.most_common():
        print(f"  {k}: {v}")

    print("\nby deployment profile:")
    for k, v in deploy_counts.most_common():
        print(f"  {k}: {v}")

    print("\nby data sensitivity:")
    for k, v in sensitivity_counts.most_common():
        print(f"  {k}: {v}")

    print("\ntop vulnerability factors:")
    for k, v in vuln_counts.most_common(20):
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
