"""Main client for CarbonCue SDK."""

from datetime import datetime, timedelta
from typing import Any

import httpx

from carboncue_sdk.config import CarbonConfig
from carboncue_sdk.models import CarbonIntensity, SCIScore


class CarbonClient:
    """Client for accessing carbon intensity data and calculating SCI scores.

    Example:
        >>> client = CarbonClient()
        >>> intensity = await client.get_current_intensity(region="us-west-2")
        >>> sci = client.calculate_sci(
        ...     operations=100.0,
        ...     materials=50.0,
        ...     functional_unit=1000,
        ...     region="us-west-2"
        ... )
    """

    def __init__(self, config: CarbonConfig | None = None) -> None:
        """Initialize the carbon client.

        Args:
            config: Optional configuration. If not provided, loads from environment.
        """
        self.config = config or CarbonConfig()
        self._http_client: httpx.AsyncClient | None = None
        self._cache: dict[str, tuple[Any, datetime]] = {}

    async def __aenter__(self) -> "CarbonClient":
        """Async context manager entry."""
        self._http_client = httpx.AsyncClient(
            timeout=self.config.request_timeout,
            headers={"auth-token": self.config.electricity_maps_api_key or ""},
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    def _get_from_cache(self, key: str) -> Any | None:
        """Get value from cache if not expired.

        Args:
            key: Cache key

        Returns:
            Cached value if exists and not expired, None otherwise
        """
        if not self.config.enable_caching:
            return None

        if key in self._cache:
            value, timestamp = self._cache[key]
            if datetime.utcnow() - timestamp < timedelta(seconds=self.config.cache_ttl_seconds):
                return value
            del self._cache[key]
        return None

    def _set_cache(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        if self.config.enable_caching:
            self._cache[key] = (value, datetime.utcnow())

    async def get_current_intensity(self, region: str, provider: str = "aws") -> CarbonIntensity:
        """Get current carbon intensity for a region.

        Args:
            region: Region code (e.g., us-west-2)
            provider: Cloud provider (aws, azure, gcp, etc.)

        Returns:
            Current carbon intensity data

        Raises:
            httpx.HTTPError: If API request fails
            ValueError: If region is invalid
        """
        cache_key = f"intensity:{provider}:{region}"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached  # type: ignore[no-any-return]

        # For now, return mock data - will integrate real APIs in implementation
        # This follows Principle VI: Prefer Existing Solutions
        # TODO: Integrate Electricity Maps API or GSF Carbon-Aware SDK
        intensity = CarbonIntensity(
            region=region,
            carbon_intensity=250.0,  # Mock: Average global grid intensity
            fossil_fuel_percentage=60.0,
            renewable_percentage=40.0,
            source="mock",  # Will be "ElectricityMaps" or "GSF SDK"
        )

        self._set_cache(cache_key, intensity)
        return intensity

    def calculate_sci(
        self,
        operational_emissions: float,
        embodied_emissions: float,
        functional_unit: float,
        functional_unit_type: str = "requests",
        region: str = "us-west-2",
    ) -> SCIScore:
        """Calculate Software Carbon Intensity (SCI) score.

        Implements GSF SCI specification: SCI = (O + M) / R

        Args:
            operational_emissions: O - Operational emissions in gCO2eq
            embodied_emissions: M - Embodied emissions in gCO2eq
            functional_unit: R - Number of functional units
            functional_unit_type: Type of functional unit (requests, users, etc.)
            region: Region where computation occurred

        Returns:
            Calculated SCI score

        Raises:
            ValueError: If functional_unit is <= 0
        """
        if functional_unit <= 0:
            raise ValueError("Functional unit must be greater than 0")

        score = (operational_emissions + embodied_emissions) / functional_unit

        return SCIScore(
            score=score,
            operational_emissions=operational_emissions,
            embodied_emissions=embodied_emissions,
            functional_unit=functional_unit,
            functional_unit_type=functional_unit_type,
            region=region,
        )

    async def close(self) -> None:
        """Close the HTTP client and cleanup resources."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None
