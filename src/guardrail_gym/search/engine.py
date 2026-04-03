from __future__ import annotations

import json
import random
from pathlib import Path

import yaml

from guardrail_gym.controls.registry import list_controls
from guardrail_gym.search.crossover import crossover
from guardrail_gym.search.fitness import evaluate_genotype
from guardrail_gym.search.genotype import Genotype
from guardrail_gym.search.mutations import mutate_add_control, mutate_remove_control, mutate_threshold, mutate_topology
from guardrail_gym.search.pareto import pareto_front

class EvoGuardSearchEngine:
    def __init__(self, benchmark, config: dict):
        self.benchmark = benchmark
        self.config = config
        self.available_controls = [c.key for c in list_controls()]
        self.base_models = config.get("base_models", ["mock-llm"])
        self.population_size = config.get("population_size", 12)
        self.generations = config.get("generations", 8)
        self.elite_k = config.get("elite_k", 4)
        self.environment_name = config["environment"]
        self.seed = config.get("seed", 7)
        random.seed(self.seed)

    @classmethod
    def from_yaml(cls, benchmark, path: str):
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return cls(benchmark, config)

    def random_genotype(self) -> Genotype:
        k = random.randint(0, min(4, len(self.available_controls)))
        controls = sorted(random.sample(self.available_controls, k=k)) if k > 0 else []
        thresholds = {c: round(random.uniform(0.4, 0.9), 2) for c in controls}
        topology = random.choice(["linear", "gated", "branching"])
        return Genotype(
            base_model=random.choice(self.base_models),
            controls=controls,
            thresholds=thresholds,
            topology=topology,
        )

    def initial_population(self) -> list[Genotype]:
        return [self.random_genotype() for _ in range(self.population_size)]

    def mutate(self, genotype: Genotype) -> Genotype:
        op = random.choice(["add", "remove", "threshold", "topology"])
        if op == "add":
            return mutate_add_control(genotype, self.available_controls)
        if op == "remove":
            return mutate_remove_control(genotype)
        if op == "threshold":
            return mutate_threshold(genotype)
        return mutate_topology(genotype)

    def run(self, output_path: str | None = None) -> dict:
        population = self.initial_population()
        history = []

        for generation in range(self.generations):
            scored = [evaluate_genotype(g, self.benchmark, self.environment_name) for g in population]
            scored = sorted(scored, key=lambda x: x["objective"], reverse=True)
            elites = scored[: self.elite_k]
            history.append({
                "generation": generation,
                "best": elites[0],
                "population": scored,
            })

            next_population = [Genotype(**elite["genotype"]) for elite in elites]

            while len(next_population) < self.population_size:
                parent_a = Genotype(**random.choice(elites)["genotype"])
                parent_b = Genotype(**random.choice(elites)["genotype"])
                child = crossover(parent_a, parent_b)
                child = self.mutate(child)
                next_population.append(child)

            population = next_population

        final_scored = [evaluate_genotype(g, self.benchmark, self.environment_name) for g in population]
        final_scored = sorted(final_scored, key=lambda x: x["objective"], reverse=True)
        front = pareto_front(final_scored, ["safety", "compliance", "utility"])

        payload = {
            "environment": self.environment_name,
            "config": self.config,
            "best": final_scored[0],
            "pareto_front": front,
            "history": history,
        }

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        return payload
