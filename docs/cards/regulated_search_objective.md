# Regulated Search Objective

The regulated EvoGuard objective now optimizes across:

- safety
- compliance
- utility
- auditability
- latency
- cost
- vulnerability coverage
- deployment feasibility
- quantization feasibility
- deployment cost penalty

## Design principle

A guardrail portfolio is evaluated not only for output quality, but for whether it is realistic to deploy for a given environment and hardware/cost envelope.

## Example tradeoffs

- Edge deployment may favor smaller quantizable models plus stronger graph constraints.
- Healthcare enterprise deployment may tolerate higher model cost if escalation coverage is stronger.
- Finance API deployment may favor compliant language/judge layers with vulnerability-sensitive routing.
