# EvoGuard Search spec

EvoGuard Search is a multi-objective evolutionary search procedure for guardrail architecture discovery.

## Search config schema

```yaml
search_name: healthcare-strict-demo
environment_name: healthcare_strict
candidate_models:
  - gpt-5.4
  - claude-sonnet-4.6
  - gemini-3.1-pro
  - llama-4-maverick
allowed_controls:
  - regex_denylist
  - schema_validator
  - medical_urgency_classifier
  - policy_compliance_judge
  - grounding_judge
  - policy_graph_router
  - adaptive_risk_controller
  - human_escalation_gate
population_size: 20
generations: 8
mutation_rate: 0.25
crossover_rate: 0.60
objective_weights:
  safety: 0.35
  compliance: 0.25
  utility: 0.10
  auditability: 0.15
  latency: 0.10
  cost: 0.05
seed: 7
```

## Genotype

A genotype contains:
- a base model
- enabled control primitives
- per-control thresholds
- execution topology

## Current scoring implementation

This scaffold includes a deterministic simulation-style scoring function for rapid prototyping. In a production benchmark, replace it with:
- benchmark execution harnesses
- real model adapters
- real judge outputs
- logged latency and cost
- domain-specific evaluation labels
