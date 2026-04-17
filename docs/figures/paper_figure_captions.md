# Paper Figure Captions

## Figure 1 — Canonical Risk Taxonomy
Eight super-domains of conversational AI risk, integrating vulnerability, regulatory, economic, informational, security, privacy, reliability, and systemic governance concerns. The taxonomy operationalizes internationally convergent AI risk framing into a conversational guardrail benchmark.

## Figure 2 — Isolation Performance by Control
Top isolated controls by environment. The figure shows that marginal guardrail value is environment-dependent: healthcare scenarios favor urgency-sensitive and escalation-capable controls, while finance scenarios place more weight on compliance and vulnerability-sensitive adaptation.

## Figure 3 — Complementarity Heatmap
Pairwise synergy among guardrail controls. Positive interactions indicate portfolios where controls provide super-additive gains; negative or near-zero regions indicate redundancy. This supports the claim that compliant conversational systems are better represented as portfolios than as single safety layers.

## Figure 4 — EvoGuard Search Progress
Best objective achieved per generation across environments. The figure illustrates how different environments select different compliance architectures under the same search process.

## Figure 5 — Pareto Frontier of Evolved Stacks
Non-dominated guardrail architectures plotted over safety and compliance, with utility encoded by point size. This demonstrates that no single architecture dominates across all objectives and motivates explicit tradeoff-aware optimization.

## Figure 6 — Best Evolved Stack by Environment
Top evolved architecture for each environment. The figure shows that healthcare, finance, adversarial, and edge-constrained deployments converge to distinct portfolios of controls.

## Figure 7 — Model Tradeoff: Objective vs Risk-Domain Coverage
Performance of model-conditioned winning stacks, showing tradeoffs between overall objective and risk-domain coverage. This highlights the importance of considering deployment and quantization feasibility alongside raw model capability.

## Figure 8 — Control Motifs in Winning Stacks
Frequency with which each guardrail primitive appears in the best evolved stacks. This summarizes which controls act as recurring “compliance motifs” across regulated conversational environments.
