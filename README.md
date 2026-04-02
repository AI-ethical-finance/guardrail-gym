![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Status](https://img.shields.io/badge/status-research-orange)
# guardrail-gym

`guardrail-gym` is a GitHub-ready, pip-installable Python package for **designing, benchmarking, and evolving conversational guardrail stacks** for regulated and high-stakes deployments.

It packages two linked ideas:

- **guardrail-gym**: a benchmark and policy-composition toolkit for conversational compliance.
- **EvoGuard Search**: a multi-objective evolutionary search engine that discovers high-performing guardrail architectures under environment-specific constraints.

## Why this package exists

Teams building conversational systems in healthcare, finance, insurance, public services, and enterprise workflows often ask:

- Which guardrail controls are worth implementing first?
- Which controls work well together?
- How much compliance architecture is justified by the deployment context?
- Does the answer change for single-model chat, RAG, or agentic systems?

`guardrail-gym` treats those questions as an experimental and optimization problem.

## Core concepts

### 1. Benchmark specification
A benchmark is defined by:
- **environment**: e.g. healthcare-strict, finance-consumer, agentic-transactional
- **system mode**: chat, rag, or agentic
- **tasks**: scenario templates with expected safe behavior and prohibited behavior
- **metrics**: safety, compliance, utility, latency, cost, and auditability

### 2. Guardrail primitives
Primitives are modular controls such as:
- regex allow/deny rules
- PHI / PII detectors
- medical urgency classifiers
- policy judges
- workflow graphs
- human escalation gates
- uncertainty-aware neurosymbolic controllers

### 3. EvoGuard Search
A candidate compliance system is encoded as a genotype over:
- a base conversational model
- a set of enabled guardrail primitives
- thresholds and hyperparameters
- execution topology

The search engine mutates, recombines, and scores these candidate systems to find Pareto-efficient stacks.

## Installation

```bash
pip install guardrail-gym
```

For development:

```bash
pip install -e .[dev]
```

## Quick start

### Inspect built-in benchmark environments

```bash
guardrail-gym benchmark list-environments
```

### Inspect built-in control primitives

```bash
guardrail-gym controls list
```

### Generate a recommendation from a deployment profile

```bash
guardrail-gym recommend examples/profile.healthcare.yaml
```

### Run EvoGuard Search on a benchmark spec

```bash
guardrail-gym search run examples/search.healthcare.yaml
```

## Minimal Python example

```python
from guardrail_gym import (
    ComplianceProfile,
    GuardrailRecommender,
    BenchmarkSpec,
    EvoGuardSearch,
)

profile = ComplianceProfile(
    domain="healthcare",
    jurisdiction=["US", "EU"],
    user_vulnerability="high",
    data_sensitivity="phi",
    autonomy="advisory",
    actionability="decision_adjacent",
    model_type="rag",
    retrieval=True,
    memory=True,
    human_review=False,
    tool_access=["ehr_lookup"],
)

recommendation = GuardrailRecommender().recommend(profile)
print(recommendation.model_dump())

benchmark = BenchmarkSpec.from_yaml("examples/benchmark.healthcare.yaml")
search = EvoGuardSearch.from_yaml("examples/search.healthcare.yaml")
result = search.run(benchmark)
print(result.best_candidates[:3])
```

## Package layout

```text
src/guardrail_gym/
  benchmark/        benchmark schemas and built-in environments
  controls/         primitive control registry
  evoguard/         genotype, mutation, crossover, search engine
  profiles/         deployment profile and recommendation logic
  cli/              Typer CLI entrypoints
```

## What is included in this scaffold

- typed benchmark spec models
- typed search config models
- built-in environment templates
- built-in control library
- risk scoring and guardrail recommendation
- evolutionary search scaffolding
- CLI for listing controls, reading benchmarks, and running search
- example YAML specs
- smoke tests

## What is intentionally left stubbed

This scaffold does **not** include proprietary model adapters, real medical or financial policy evaluation backends, or production-grade classifier weights. It is a clean reference architecture intended for research and internal prototyping.

## Suggested GitHub repo structure

- `README.md` for project overview and install instructions
- `docs/benchmark_spec.md` for benchmark schema
- `docs/evoguard_search.md` for search algorithm and genotype design
- `examples/` for ready-to-run YAML configs
- `tests/` for smoke tests and schema validation

## License

MIT
