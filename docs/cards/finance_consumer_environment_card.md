# Environment Card: finance_consumer

## Search configuration
- search_name: finance_search_v1
- candidate_models: ['mock-llm', 'gpt-like', 'claude-like']
- allowed_controls: ['regex_denylist', 'schema_validator', 'phi_detector', 'medical_urgency_classifier', 'financial_vulnerability_classifier', 'policy_compliance_judge', 'grounding_judge', 'policy_graph_router', 'tool_approval_graph', 'adaptive_risk_controller', 'human_escalation_gate', 'audit_logger']
- objective_weights: {'safety': 0.38, 'compliance': 0.32, 'utility': 0.15, 'latency': 0.1, 'cost': 0.05}

## Notes
This card documents the search environment and optimization weighting used in EvoGuard experiments.
