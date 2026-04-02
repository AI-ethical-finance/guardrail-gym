from __future__ import annotations

import random
from pathlib import Path

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.controls.registry import CONTROL_LIBRARY
from guardrail_gym.evoguard.schemas import CandidateGenome, ScoredCandidate, SearchConfig, SearchResult


class EvoGuardSearch:
    def __init__(self, config: SearchConfig):
        self.config = config
        self._rng = random.Random(config.seed)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "EvoGuardSearch":
        return cls(SearchConfig.from_yaml(path))

    def _random_genome(self) -> CandidateGenome:
        base_model = self._rng.choice(self.config.candidate_models)
        n_controls = self._rng.randint(1, max(1, min(5, len(self.config.allowed_controls))))
        enabled = sorted(self._rng.sample(self.config.allowed_controls, n_controls))
        topology = self._rng.choice(["linear", "graph", "hybrid"])
        thresholds = {key: round(self._rng.uniform(0.4, 0.95), 2) for key in enabled[:2]}
        return CandidateGenome(
            base_model=base_model,
            enabled_controls=enabled,
            thresholds=thresholds,
            topology=topology,
        )

    def _score_candidate(self, genome: CandidateGenome, benchmark: BenchmarkSpec) -> ScoredCandidate:
        control_families = [CONTROL_LIBRARY[c].family for c in genome.enabled_controls if c in CONTROL_LIBRARY]
        family_bonus = len(set(control_families)) * 0.08
        graph_bonus = 0.12 if genome.topology in {"graph", "hybrid"} else 0.02
        scenario_factor = min(len(benchmark.scenarios) / 20.0, 1.0)
        env_factor = 0.1 * len(benchmark.environments)
        safety = min(0.35 + family_bonus + graph_bonus + 0.05 * scenario_factor, 0.99)
        compliance = min(0.30 + family_bonus + 0.08 * env_factor, 0.99)
        utility = max(0.85 - 0.04 * len(genome.enabled_controls), 0.40)
        latency = min(0.10 + 0.05 * len(genome.enabled_controls), 0.99)
        cost = min(0.12 + 0.04 * len(genome.enabled_controls), 0.99)
        auditability = min(0.25 + 0.10 * sum(f in {"deterministic", "graph", "human_system"} for f in control_families), 0.99)

        weights = self.config.objective_weights
        fitness = (
            weights.get("safety", 0.3) * safety
            + weights.get("compliance", 0.25) * compliance
            + weights.get("utility", 0.15) * utility
            + weights.get("auditability", 0.15) * auditability
            - weights.get("latency", 0.10) * latency
            - weights.get("cost", 0.05) * cost
        )
        return ScoredCandidate(
            genome=genome,
            scores={
                "safety": round(safety, 3),
                "compliance": round(compliance, 3),
                "utility": round(utility, 3),
                "latency": round(latency, 3),
                "cost": round(cost, 3),
                "auditability": round(auditability, 3),
            },
            fitness=round(fitness, 4),
        )

    def _mutate(self, genome: CandidateGenome) -> CandidateGenome:
        controls = set(genome.enabled_controls)
        if self._rng.random() < 0.5 and len(controls) < len(self.config.allowed_controls):
            controls.add(self._rng.choice(self.config.allowed_controls))
        elif controls:
            controls.discard(self._rng.choice(sorted(controls)))
            if not controls:
                controls.add(self._rng.choice(self.config.allowed_controls))

        topology = genome.topology
        if self._rng.random() < 0.3:
            topology = self._rng.choice(["linear", "graph", "hybrid"])

        thresholds = dict(genome.thresholds)
        if controls:
            chosen = self._rng.choice(sorted(controls))
            thresholds[chosen] = round(self._rng.uniform(0.4, 0.95), 2)

        return CandidateGenome(
            base_model=genome.base_model if self._rng.random() > 0.2 else self._rng.choice(self.config.candidate_models),
            enabled_controls=sorted(controls),
            thresholds=thresholds,
            topology=topology,
        )

    def _crossover(self, a: CandidateGenome, b: CandidateGenome) -> CandidateGenome:
        controls = sorted(set(a.enabled_controls).union(b.enabled_controls))
        if len(controls) > 6:
            controls = sorted(self._rng.sample(controls, 6))
        thresholds = {**a.thresholds, **b.thresholds}
        return CandidateGenome(
            base_model=self._rng.choice([a.base_model, b.base_model]),
            enabled_controls=controls,
            thresholds=thresholds,
            topology=self._rng.choice([a.topology, b.topology]),
        )

    def run(self, benchmark: BenchmarkSpec) -> SearchResult:
        population = [self._random_genome() for _ in range(self.config.population_size)]
        best: list[ScoredCandidate] = []

        for _ in range(self.config.generations):
            scored = [self._score_candidate(g, benchmark) for g in population]
            scored.sort(key=lambda x: x.fitness, reverse=True)
            best = sorted(best + scored, key=lambda x: x.fitness, reverse=True)[:10]
            elites = [s.genome for s in scored[: max(2, self.config.population_size // 5)]]
            next_population = elites.copy()
            while len(next_population) < self.config.population_size:
                if self._rng.random() < self.config.crossover_rate and len(elites) >= 2:
                    parent_a, parent_b = self._rng.sample(elites, 2)
                    child = self._crossover(parent_a, parent_b)
                else:
                    child = self._rng.choice(elites)
                if self._rng.random() < self.config.mutation_rate:
                    child = self._mutate(child)
                next_population.append(child)
            population = next_population[: self.config.population_size]

        return SearchResult(
            search_name=self.config.search_name,
            environment_name=self.config.environment_name,
            generations=self.config.generations,
            best_candidates=best,
            population_summary={
                "population_size": self.config.population_size,
                "candidate_models": len(self.config.candidate_models),
                "allowed_controls": len(self.config.allowed_controls),
            },
        )
