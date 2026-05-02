from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.eval.coverage import coverage_payload
from guardrail_gym.search.engine import EvoGuardSearchEngine

BENCHMARK = "examples/benchmark.regulated.search.yaml"
MODEL_SUITE = "examples/model_simulation_suite.yaml"

BASE_CONFIGS = {
    "healthcare_strict": "examples/search.healthcare_regulated.yaml",
    "finance_consumer": "examples/search.finance_regulated.yaml",
    "adversarial": "examples/search.edge_regulated.yaml",
}

OUT_DIR = Path("results/model_stack_simulations")


def flatten_models(suite: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for group, models in suite["model_groups"].items():
        for model in models:
            row = dict(model)
            row["group"] = group
            out.append(row)
    return out


def choose_deployment(model: dict[str, Any]) -> str:
    modes = model.get("deployment_modes", []) or model.get("deployment", []) or []
    if "edge_device" in modes:
        return "edge_device"
    if "enterprise_gpu" in modes:
        return "enterprise_gpu"
    if "api_hosted" in modes:
        return "api_hosted"
    return "api_hosted"


def choose_quantization(model: dict[str, Any]) -> str:
    profiles = model.get("quantization_profiles", []) or model.get("precision_profiles", []) or []
    if "int4" in profiles:
        return "int4"
    if "fp8" in profiles:
        return "fp8"
    if "int8" in profiles:
        return "int8"
    if "managed" in profiles:
        return "managed"
    if "bf16" in profiles:
        return "bf16"
    return "managed"


def scenarios_for_environment(benchmark: BenchmarkSpec, env_name: str):
    return benchmark.scenarios_for_environment(env_name)


def main():
    benchmark = BenchmarkSpec.from_yaml(BENCHMARK)
    suite = yaml.safe_load(open(MODEL_SUITE, "r", encoding="utf-8"))
    models = flatten_models(suite)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = []

    for env, config_path in BASE_CONFIGS.items():
        base_config = yaml.safe_load(open(config_path, "r", encoding="utf-8"))
        env_scenarios = scenarios_for_environment(benchmark, env)

        for model in models:
            config = dict(base_config)
            config["candidate_models"] = [model["key"]]
            config["environment_name"] = env
            config["deployment_profile"] = choose_deployment(model)
            config["quantization_profile"] = choose_quantization(model)

            # Stable paper-simulation settings.
            config["population_size"] = int(config.get("population_size", 14))
            config["generations"] = int(config.get("generations", 8))
            config["elite_k"] = int(config.get("elite_k", 4))

            engine = EvoGuardSearchEngine(benchmark, config)
            payload = engine.run()

            best = payload["best"]
            genotype = best["genotype"]
            cov = coverage_payload(genotype, env_scenarios)

            row = {
                "environment": env,
                "model": model["key"],
                "model_group": model["group"],
                "deployment_profile": config["deployment_profile"],
                "quantization_profile": config["quantization_profile"],
                "objective": best.get("objective"),
                "safety": best.get("safety"),
                "compliance": best.get("compliance"),
                "utility": best.get("utility"),
                "latency": best.get("latency"),
                "cost": best.get("cost"),
                "auditability": best.get("auditability"),
                "vulnerability_coverage": best.get("vulnerability_coverage", cov["vulnerability_coverage"]),
                "risk_domain_coverage": best.get("risk_domain_coverage", cov["risk_domain_coverage"]),
                "cognitive_role_coverage": best.get("cognitive_role_coverage"),
                "stack_order_score": best.get("stack_order_score"),
                "layer_diversity": best.get("layer_diversity"),
                "deployment_feasibility": best.get("deployment_feasibility"),
                "quantization_feasibility": best.get("quantization_feasibility"),
                "deployment_cost_penalty": best.get("deployment_cost_penalty"),
                "num_controls": len(genotype.get("controls", [])),
                "controls": genotype.get("controls", []),
                "control_layers": genotype.get("control_layers", {}),
                "activation_conditions": genotype.get("activation_conditions", {}),
            }
            summary.append(row)

            out_path = OUT_DIR / f"{env}__{model['key'].replace('/', '_')}.json"
            out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print("done", env, model["key"], "objective", row["objective"])

    summary_path = OUT_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("wrote", summary_path)


if __name__ == "__main__":
    main()
