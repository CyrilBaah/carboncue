"""Data models for CarbonCue SDK."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CloudProvider = Literal["aws", "azure", "gcp", "digitalocean", "other"]


class Region(BaseModel):
    """Cloud region information."""

    model_config = ConfigDict(frozen=True)

    code: str = Field(..., description="Region code (e.g., us-west-2)")
    provider: CloudProvider = Field(..., description="Cloud provider")
    location: str | None = Field(None, description="Geographic location")


class CarbonIntensity(BaseModel):
    """Carbon intensity data for a specific region and time."""

    model_config = ConfigDict(frozen=True)

    region: str = Field(..., description="Region code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Measurement time")
    carbon_intensity: float = Field(..., gt=0, description="gCO2eq/kWh")
    fossil_fuel_percentage: float | None = Field(
        None, ge=0, le=100, description="Percentage of fossil fuel in energy mix"
    )
    renewable_percentage: float | None = Field(
        None, ge=0, le=100, description="Percentage of renewable energy in mix"
    )
    source: str = Field(..., description="Data source (e.g., ElectricityMaps, GSF SDK)")


class SCIScore(BaseModel):
    """Software Carbon Intensity (SCI) score per GSF specification.

    SCI = (O + M) / R
    Where:
        O = Operational emissions (energy × carbon intensity)
        M = Embodied emissions (manufacturing impact)
        R = Functional unit (requests, users, etc.)
    """

    model_config = ConfigDict(frozen=True)

    score: float = Field(..., ge=0, description="SCI score (gCO2eq per functional unit)")
    operational_emissions: float = Field(..., ge=0, description="O: Operational emissions (gCO2eq)")
    embodied_emissions: float = Field(..., ge=0, description="M: Embodied emissions (gCO2eq)")
    functional_unit: float = Field(..., gt=0, description="R: Functional unit count")
    functional_unit_type: str = Field(
        ..., description="Type of functional unit (requests, users, etc.)"
    )
    region: str = Field(..., description="Region where computation occurred")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Calculation time")


class EmissionsBreakdown(BaseModel):
    """Detailed breakdown of carbon emissions."""

    model_config = ConfigDict(frozen=True)

    total_emissions: float = Field(..., ge=0, description="Total emissions (gCO2eq)")
    compute_emissions: float = Field(..., ge=0, description="Compute/CPU emissions")
    storage_emissions: float = Field(..., ge=0, description="Storage emissions")
    network_emissions: float = Field(..., ge=0, description="Network transfer emissions")
    memory_emissions: float = Field(..., ge=0, description="Memory usage emissions")
