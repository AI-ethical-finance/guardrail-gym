from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List


@dataclass
class LayerAssignment:
    layer: str
    controls: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LayeredStack:
    base_model: str
    topology: str
    layers: List[LayerAssignment] = field(default_factory=list)
    thresholds: Dict[str, float] = field(default_factory=dict)
    activation_conditions: Dict[str, str] = field(default_factory=dict)

    def all_controls(self) -> List[str]:
        out = []
        for layer in self.layers:
            out.extend(layer.controls)
        return out

    def to_dict(self) -> dict:
        return {
            "base_model": self.base_model,
            "topology": self.topology,
            "layers": [l.to_dict() for l in self.layers],
            "thresholds": self.thresholds,
            "activation_conditions": self.activation_conditions,
        }
