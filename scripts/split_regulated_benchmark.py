from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import random

from guardrail_gym.benchmark.spec import BenchmarkSpec

SOURCE = "examples/benchmark.regulated.yaml"
SEARCH_OUT = "examples/benchmark.regulated.search.yaml"
EVAL_OUT = "examples/benchmark.regulated.eval.yaml"
SEED = 42
SEARCH_FRACTION = 0.7


def scenario_bucket_key(s):
    env = s.effective_environment() or "none"
    domain = s.domain
    risks = tuple(sorted(s.risk_domains)) if getattr(s, "risk_domains", None) else ()
    vulns = tuple(sorted(s.vulnerability_factors)) if getattr(s, "vulnerability_factors", None) else ()
    return (env, domain, risks, vulns)


def main():
    random.seed(SEED)
    benchmark = BenchmarkSpec.from_yaml(SOURCE)

    buckets = defaultdict(list)
    for scenario in benchmark.scenarios:
        buckets[scenario_bucket_key(scenario)].append(scenario)

    search_scenarios = []
    eval_scenarios = []

    for _, items in buckets.items():
        random.shuffle(items)
        k = max(1, int(len(items) * SEARCH_FRACTION)) if len(items) > 1 else 1
        search_scenarios.extend(items[:k])
        eval_scenarios.extend(items[k:])

    search_spec = BenchmarkSpec(
        benchmark_name=f"{benchmark.benchmark_name}_search",
        version=benchmark.version,
        environments=benchmark.environments,
        scenarios=search_scenarios,
    )
    eval_spec = BenchmarkSpec(
        benchmark_name=f"{benchmark.benchmark_name}_eval",
        version=benchmark.version,
        environments=benchmark.environments,
        scenarios=eval_scenarios,
    )

    search_spec.write_yaml(SEARCH_OUT)
    eval_spec.write_yaml(EVAL_OUT)

    print("source scenarios:", len(benchmark.scenarios))
    print("search scenarios:", len(search_scenarios))
    print("eval scenarios:", len(eval_scenarios))
    print("wrote", SEARCH_OUT)
    print("wrote", EVAL_OUT)


if __name__ == "__main__":
    main()
