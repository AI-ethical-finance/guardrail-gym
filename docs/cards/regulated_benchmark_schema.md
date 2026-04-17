# Regulated Benchmark Schema

The benchmark schema now supports regulated-risk scenario attributes directly.

## Added scenario fields
- `environment`
- `deployment_profile`
- `vulnerability_factors`
- `decision_context`
- `data_sensitivity`
- `harm_modes`

## Purpose
These fields allow the benchmark, search engine, and evaluation pipeline to reason about:
- vulnerability-sensitive conditions
- deployment realism
- cross-domain harm types
- many-to-many guardrail coverage

## Example use cases
- filter scenarios involving bereavement
- filter scenarios for edge deployment
- search for stacks optimized for chronic illness + low support network
- compare healthcare_strict and finance_consumer under quantization constraints
