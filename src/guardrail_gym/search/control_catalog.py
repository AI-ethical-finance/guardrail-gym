from __future__ import annotations

from pathlib import Path
import yaml


CATALOG_PATH = Path("risk_ontology/expanded_control_catalog.yaml")


def load_control_catalog() -> dict:
    return yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))["controls"]


def control_default_layer(control_key: str) -> str:
    catalog = load_control_catalog()
    return catalog.get(control_key, {}).get("default_layer", "output_verification")


def control_family(control_key: str) -> str:
    catalog = load_control_catalog()
    return catalog.get(control_key, {}).get("family", "unknown")
