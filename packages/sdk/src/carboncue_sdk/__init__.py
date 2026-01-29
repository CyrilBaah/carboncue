"""CarbonCue SDK - Core library for carbon-aware computing."""

from carboncue_sdk.client import CarbonClient
from carboncue_sdk.config import CarbonConfig
from carboncue_sdk.exceptions import (
    APIError,
    AuthenticationError,
    CarbonCueError,
    DataNotAvailableError,
    InvalidProviderError,
    InvalidRegionError,
    RateLimitError,
)
from carboncue_sdk.models import CarbonIntensity, Region, SCIScore
from carboncue_sdk.region_mapper import RegionMapper

__version__ = "1.1.0"
__all__ = [
    "CarbonClient",
    "CarbonIntensity",
    "SCIScore",
    "Region",
    "CarbonConfig",
    "RegionMapper",
    "CarbonCueError",
    "APIError",
    "InvalidRegionError",
    "InvalidProviderError",
    "RateLimitError",
    "AuthenticationError",
    "DataNotAvailableError",
]
