from __future__ import annotations

from collections import Counter

from guardrail_gym.benchmark.spec import BenchmarkSpec

FILES = [
    "examples/benchmark.regulated.search.yaml",
    "examples/benchmark.regulated.eval.yaml",
]


def summarize(path: str):
    b = BenchmarkSpec.from_yaml(path)
    env_counts = Counter()
    risk_counts = Counter()
    vuln_counts = Counter()

    for s in b.scenarios:
        env_counts[s.effective_environment()] += 1
        for r in getattr(s, "risk_domains", []) or []:
            risk_counts[r] += 1
        for v in getattr(s, "vulnerability_factors", []) or []:
            vuln_counts[v] += 1

    print("=" * 80)
    print(path)
    print("scenarios:", len(b.scenarios))
    print("by environment:", dict(env_counts))
    print("top risk domains:", risk_counts.most_common(10))
    print("top vulnerabilities:", vuln_counts.most_common(10))


def main():
    for path in FILES:
        summarize(path)


if __name__ == "__main__":
    main()
