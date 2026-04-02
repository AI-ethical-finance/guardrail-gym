from __future__ import annotations

from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.table import Table

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.controls.registry import list_controls
from guardrail_gym.evoguard.schemas import SearchConfig
from guardrail_gym.evoguard.search import EvoGuardSearch
from guardrail_gym.profiles.recommend import GuardrailRecommender
from guardrail_gym.profiles.schemas import ComplianceProfile

app = typer.Typer(help="guardrail-gym command line interface")
benchmark_app = typer.Typer(help="Benchmark specification commands")
controls_app = typer.Typer(help="Control registry commands")
search_app = typer.Typer(help="Evolutionary search commands")
app.add_typer(benchmark_app, name="benchmark")
app.add_typer(controls_app, name="controls")
app.add_typer(search_app, name="search")
console = Console()


@app.command()
def recommend(profile_path: Path) -> None:
    """Generate a guardrail recommendation from a YAML profile."""
    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    profile = ComplianceProfile.model_validate(data)
    rec = GuardrailRecommender().recommend(profile)
    console.print_json(data=rec.model_dump_json())


@benchmark_app.command("list-environments")
def list_environments(spec_path: Path = Path("examples/benchmark.healthcare.yaml")) -> None:
    """List environments from a benchmark YAML spec."""
    spec = BenchmarkSpec.from_yaml(spec_path)
    table = Table(title=f"Benchmark environments: {spec.benchmark_name}")
    table.add_column("Name")
    table.add_column("Description")
    for env in spec.environments:
        table.add_row(env.name, env.description)
    console.print(table)


@controls_app.command("list")
def show_controls() -> None:
    """List built-in control primitives."""
    table = Table(title="Built-in control primitives")
    table.add_column("Key")
    table.add_column("Family")
    table.add_column("Placement")
    table.add_column("Description")
    for control in list_controls():
        table.add_row(control.key, control.family, control.placement, control.description)
    console.print(table)


@search_app.command("run")
def run_search(search_config_path: Path, benchmark_path: Path) -> None:
    """Run EvoGuard Search on a benchmark spec."""
    search = EvoGuardSearch(SearchConfig.from_yaml(search_config_path))
    benchmark = BenchmarkSpec.from_yaml(benchmark_path)
    result = search.run(benchmark)
    console.print_json(data=result.model_dump_json())


if __name__ == "__main__":
    app()
