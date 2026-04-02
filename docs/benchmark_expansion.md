# Expanded benchmark layer

This patch adds:

- an expanded benchmark specification with `scenario_tags`, `disclosure_requirements`, and `escalation_required`
- synthetic environment-weighted scoring for isolation and complementarity studies
- CSV/JSON report writers
- CLI commands:
  - `guardrail-gym benchmark run-isolation`
  - `guardrail-gym benchmark run-complementarity`
- scripts:
  - `python scripts/run_isolation.py`
  - `python scripts/run_complementarity.py`

The new runners are synthetic research scaffolds. They estimate the likely impact of control stacks based on scenario structure, environment weights, and guardrail family assumptions. They are designed to be replaced later with execution-backed evaluations over real model adapters.
