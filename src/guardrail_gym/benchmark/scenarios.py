from __future__ import annotations

from pathlib import Path

from guardrail_gym.benchmark.spec import BenchmarkSpec


def load_benchmark(path: str | Path) -> BenchmarkSpec:
    return BenchmarkSpec.from_yaml(path)
