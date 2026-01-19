"""Main CLI entry point for CarbonCue."""

import asyncio

import click
from carboncue_sdk import CarbonClient, CarbonConfig
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="carboncue")
def cli() -> None:
    """CarbonCue - Carbon-aware development tools.

    Measure and reduce the carbon footprint of your software based on
    Green Software Foundation (GSF) principles.
    """
    pass


@cli.command()
@click.option(
    "--region",
    "-r",
    default="us-west-2",
    help="Cloud region to check (e.g., us-west-2, eu-west-1)",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["aws", "azure", "gcp", "digitalocean", "other"]),
    default="aws",
    help="Cloud provider",
)
def check(region: str, provider: str) -> None:
    """Check current carbon intensity for a region.

    Example:
        carboncue check --region us-west-2 --provider aws
    """
    asyncio.run(_check_intensity(region, provider))


async def _check_intensity(region: str, provider: str) -> None:
    """Async implementation of check command."""
    with console.status(f"[bold green]Fetching carbon intensity for {region}..."):
        async with CarbonClient() as client:
            intensity = await client.get_current_intensity(region=region, provider=provider)

    # Create rich table for display
    table = Table(title=f"Carbon Intensity: {region} ({provider})")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Carbon Intensity", f"{intensity.carbon_intensity:.2f} gCO2eq/kWh")
    table.add_row("Timestamp", intensity.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"))

    if intensity.fossil_fuel_percentage is not None:
        table.add_row("Fossil Fuel %", f"{intensity.fossil_fuel_percentage:.1f}%")
    if intensity.renewable_percentage is not None:
        table.add_row("Renewable %", f"{intensity.renewable_percentage:.1f}%")

    table.add_row("Source", intensity.source)

    console.print(table)

    # Provide interpretation
    if intensity.carbon_intensity < 100:
        status = "[green]Excellent[/green] - Grid is very clean"
    elif intensity.carbon_intensity < 300:
        status = "[yellow]Moderate[/yellow] - Average grid intensity"
    else:
        status = "[red]High[/red] - Consider deferring non-critical workloads"

    console.print(f"\nStatus: {status}")


@cli.command()
@click.option(
    "--operations", "-o", type=float, required=True, help="Operational emissions (gCO2eq)"
)
@click.option("--materials", "-m", type=float, required=True, help="Embodied emissions (gCO2eq)")
@click.option("--functional-unit", "-r", type=float, required=True, help="Functional unit count")
@click.option(
    "--unit-type",
    "-t",
    default="requests",
    help="Functional unit type (requests, users, etc.)",
)
@click.option("--region", default="us-west-2", help="Region for calculation")
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["aws", "azure", "gcp", "digitalocean", "other"]),
    default="aws",
    help="Cloud provider",
)
def sci(
    operations: float,
    materials: float,
    functional_unit: float,
    unit_type: str,
    region: str,
    provider: str,  # noqa: ARG001 - Reserved for future API integration
) -> None:
    """Calculate Software Carbon Intensity (SCI) score.

    SCI = (O + M) / R per GSF specification

    Example:
        carboncue sci -o 100 -m 50 -r 1000 -t requests --region us-west-2
    """
    client = CarbonClient()
    score = client.calculate_sci(
        operational_emissions=operations,
        embodied_emissions=materials,
        functional_unit=functional_unit,
        functional_unit_type=unit_type,
        region=region,
    )

    # Display SCI breakdown
    panel = Panel.fit(
        f"""[bold cyan]SCI Score: {score.score:.4f} gCO2eq/{unit_type}[/bold cyan]

[yellow]Formula:[/yellow] SCI = (O + M) / R

[green]Breakdown:[/green]
  O (Operational): {score.operational_emissions:.2f} gCO2eq
  M (Embodied):    {score.embodied_emissions:.2f} gCO2eq
  R (Functional):  {score.functional_unit:.0f} {unit_type}

[blue]Region:[/blue] {score.region}
[blue]Timestamp:[/blue] {score.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")}
        """,
        title="🌱 SCI Calculation Result",
        border_style="green",
    )

    console.print(panel)

    # Provide recommendations
    console.print("\n[bold]Recommendations:[/bold]")
    if score.score < 0.1:
        console.print(
            "✅ [green]Excellent score! Your software is highly carbon-efficient.[/green]"
        )
    elif score.score < 1.0:
        console.print("⚠️  [yellow]Moderate score. Consider optimizing heavy operations.[/yellow]")
    else:
        console.print(
            "❌ [red]High carbon intensity. Review architecture and defer workloads to low-carbon periods.[/red]"
        )


@cli.command()
def config() -> None:
    """Show current configuration."""
    cfg = CarbonConfig()

    table = Table(title="CarbonCue Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Default Region", cfg.default_region)
    table.add_row("Default Provider", cfg.default_cloud_provider)
    table.add_row(
        "Electricity Maps API Key",
        (
            "***" + cfg.electricity_maps_api_key[-4:]
            if cfg.electricity_maps_api_key
            else "[red]Not Set[/red]"
        ),
    )
    table.add_row("Cache Enabled", str(cfg.enable_caching))
    table.add_row("Cache TTL", f"{cfg.cache_ttl_seconds}s")
    table.add_row("Request Timeout", f"{cfg.request_timeout}s")

    console.print(table)

    if not cfg.electricity_maps_api_key:
        console.print(
            "\n[yellow]⚠️  Set CARBONCUE_ELECTRICITY_MAPS_API_KEY environment variable for real-time data[/yellow]"
        )


if __name__ == "__main__":
    cli()
