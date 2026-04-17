from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List


@dataclass
class Genotype:
    base_model: str
    controls: List[str]
    thresholds: Dict[str, float] = field(default_factory=dict)
    topology: str = "linear"
    control_layers: Dict[str, str] = field(default_factory=dict)
    activation_conditions: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)
