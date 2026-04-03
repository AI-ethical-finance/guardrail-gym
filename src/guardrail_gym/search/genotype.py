from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Dict, List

@dataclass
class Genotype:
    base_model: str
    controls: List[str]
    thresholds: Dict[str, float] = field(default_factory=dict)
    topology: str = "linear"

    def to_dict(self) -> dict:
        return asdict(self)
