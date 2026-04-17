# Regulated Risk Expansion

This expansion introduces a many-to-many vulnerability and control framework for regulated conversational systems.

## Added ontology families
- health_and_disability
- behavioral_health
- life_event_shock
- abuse_and_coercion
- financial_fragility
- capability_and_comprehension
- resilience
- support_network_fragility

## Added model catalog dimensions
- deployment_modes
- precision_profiles
- cost_tier
- edge_feasibility

## Key design principle
Guardrails do not map one-to-one to risks. A single control may cover:
- detection
- adaptation
- constraint
- escalation
- evidence

## New experimental objective
Optimize not only safety/compliance/utility, but also:
- vulnerability coverage
- deployment feasibility
- quantization feasibility
- cost penalty
