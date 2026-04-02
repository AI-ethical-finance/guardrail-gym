from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class CandidateGenome(BaseModel):
    base_model: str
    enabled_controls: list[str]
    thresholds: dict[str, float] = Field(default_factory=dict)
    topology: Literal["linear", "graph", "hybrid"] = "linear"


class SearchConfig(BaseModel):
    search_name: str
    environment_name: str
    candidate_models: list[str]
    allowed_controls: list[str]
    population_size: int = 24
    generations: int = 8
    mutation_rate: float = 0.25
    crossover_rate: float = 0.60
    objective_weights: dict[str, float]
    seed: int = 7

    @classmethod
    def from_yaml(cls, path: str | Path) -> "SearchConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)


class ScoredCandidate(BaseModel):
    genome: CandidateGenome
    scores: dict[str, float]
    fitness: float


class SearchResult(BaseModel):
    search_name: str
    environment_name: str
    generations: int
    best_candidates: list[ScoredCandidate]
    population_summary: dict[str, float | int | str] = Field(default_factory=dict)
