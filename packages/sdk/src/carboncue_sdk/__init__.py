"""CarbonCue SDK - Core library for carbon-aware computing."""

from carboncue_sdk.client import CarbonClient
from carboncue_sdk.config import CarbonConfig
from carboncue_sdk.models import CarbonIntensity, Region, SCIScore

__version__ = "0.1.0"
__all__ = ["CarbonClient", "CarbonIntensity", "SCIScore", "Region", "CarbonConfig"]
