from __future__ import annotations

from typing import Dict, List

from guardrail_gym.search.control_catalog import control_default_layer
from guardrail_gym.search.stack_schema import LayerAssignment, LayeredStack


LAYER_ORDER = [
    "input_detection",
    "semantic_interpretation",
    "routing_constraint",
    "generation",
    "output_verification",
    "escalation",
    "audit_monitoring",
]


def build_layered_stack(genotype) -> LayeredStack:
    buckets: Dict[str, List[str]] = {layer: [] for layer in LAYER_ORDER}

    for control in genotype.controls:
        layer = genotype.control_layers.get(control, control_default_layer(control))
        buckets.setdefault(layer, [])
        buckets[layer].append(control)

    layers = [LayerAssignment(layer=layer, controls=buckets[layer]) for layer in LAYER_ORDER if buckets[layer]]

    return LayeredStack(
        base_model=genotype.base_model,
        topology=genotype.topology,
        layers=layers,
        thresholds=genotype.thresholds,
        activation_conditions=genotype.activation_conditions,
    )
