from __future__ import annotations

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.eval.isolation import run_isolation_study
from guardrail_gym.eval.reports import write_csv, write_json


def main() -> None:
    spec = BenchmarkSpec.from_yaml("examples/benchmark.expanded.yaml")
    for env in ["healthcare_strict", "finance_consumer", "adversarial"]:
        rows = run_isolation_study(spec, env)
        write_json(f"results/isolation_{env}.json", rows)
        write_csv(f"results/isolation_{env}.csv", rows)
        print(f"wrote results/isolation_{env}.json")


if __name__ == "__main__":
    main()
