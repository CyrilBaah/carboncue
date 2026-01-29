"""Main client for CarbonCue SDK."""

from datetime import datetime, timedelta
from typing import Any

import httpx

from carboncue_sdk.config import CarbonConfig
from carboncue_sdk.exceptions import (
    APIError,
    AuthenticationError,
    DataNotAvailableError,
    InvalidProviderError,
    InvalidRegionError,
    RateLimitError,
)
from carboncue_sdk.models import CarbonIntensity, SCIScore
from carboncue_sdk.region_mapper import RegionMapper


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
            InvalidRegionError: If region is not supported
            InvalidProviderError: If provider is not supported
            AuthenticationError: If API key is missing or invalid
            RateLimitError: If API rate limit exceeded
            DataNotAvailableError: If data not available for region
            APIError: If API request fails
        """
        cache_key = f"intensity:{provider}:{region}"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached  # type: ignore[no-any-return]

        # Map cloud region to Electricity Maps zone
        try:
            zone_id = RegionMapper.get_zone_id(region, provider)
        except ValueError as e:
            error_msg = str(e)
            if "cloud provider" in error_msg.lower():
                raise InvalidProviderError(error_msg) from e
            raise InvalidRegionError(error_msg) from e

        # Get data from Electricity Maps API
        intensity = await self._fetch_from_electricity_maps(zone_id, region)

        self._set_cache(cache_key, intensity)
        return intensity

    async def _fetch_from_electricity_maps(
        self, zone_id: str, original_region: str
    ) -> CarbonIntensity:
        """Fetch carbon intensity from Electricity Maps API.

        Args:
            zone_id: Electricity Maps zone identifier
            original_region: Original cloud region code

        Returns:
            Carbon intensity data

        Raises:
            AuthenticationError: If API key is missing or invalid
            RateLimitError: If API rate limit exceeded
            DataNotAvailableError: If data not available
            APIError: If API request fails
        """
        if not self.config.electricity_maps_api_key:
            raise AuthenticationError(
                "Electricity Maps API key not configured. "
                "Set CARBONCUE_ELECTRICITY_MAPS_API_KEY environment variable."
            )

        if not self._http_client:
            raise APIError("HTTP client not initialized. Use async context manager.")

        url = f"{self.config.electricity_maps_base_url}/carbon-intensity/latest"
        params = {"zone": zone_id}

        try:
            response = await self._http_client.get(url, params=params)

            # Handle rate limiting
            if response.status_code == 429:
                raise RateLimitError(
                    "Electricity Maps API rate limit exceeded. Please try again later."
                )

            # Handle authentication errors
            if response.status_code == 401:
                raise AuthenticationError("Invalid Electricity Maps API key.")

            # Handle data not available
            if response.status_code == 404:
                raise DataNotAvailableError(
                    f"Carbon intensity data not available for zone: {zone_id}"
                )

            # Raise for other errors
            response.raise_for_status()

            data = response.json()

            # Extract data from Electricity Maps response
            carbon_intensity = data.get("carbonIntensity")
            fossil_fuel_pct = data.get("fossilFuelPercentage")
            renewable_pct = data.get("renewablePercentage")

            if carbon_intensity is None:
                raise DataNotAvailableError(
                    f"Carbon intensity value missing in response for zone: {zone_id}"
                )

            return CarbonIntensity(
                region=original_region,
                carbon_intensity=float(carbon_intensity),
                fossil_fuel_percentage=float(fossil_fuel_pct) if fossil_fuel_pct else None,
                renewable_percentage=float(renewable_pct) if renewable_pct else None,
                source="ElectricityMaps",
            )

        except httpx.HTTPError as e:
            if isinstance(e, (RateLimitError, AuthenticationError, DataNotAvailableError)):
                raise
            raise APIError(f"Failed to fetch carbon intensity data: {str(e)}") from e

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
