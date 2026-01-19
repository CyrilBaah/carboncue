"""Integration tests for CarbonCue SDK."""

import pytest
from carboncue_sdk import CarbonClient, CarbonConfig


@pytest.mark.asyncio
@pytest.mark.integration
async def test_end_to_end_carbon_check() -> None:
    """Test end-to-end carbon intensity check workflow."""
    config = CarbonConfig(
        electricity_maps_api_key="test-key",
        enable_caching=True,
    )

    async with CarbonClient(config=config) as client:
        # Get carbon intensity
        intensity = await client.get_current_intensity(region="us-west-2", provider="aws")

        assert intensity is not None
        assert intensity.carbon_intensity > 0
        assert intensity.region == "us-west-2"

        # Calculate SCI score based on intensity
        sci = client.calculate_sci(
            operational_emissions=intensity.carbon_intensity * 10,  # Mock calculation
            embodied_emissions=50.0,
            functional_unit=100,
            functional_unit_type="requests",
            region="us-west-2",
        )

        assert sci.score > 0
        assert sci.region == "us-west-2"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_caching_behavior() -> None:
    """Test that caching works correctly."""
    config = CarbonConfig(
        electricity_maps_api_key="test-key",
        enable_caching=True,
        cache_ttl_seconds=60,
    )

    async with CarbonClient(config=config) as client:
        # First call - should fetch from API
        intensity1 = await client.get_current_intensity(region="us-west-2")

        # Second call - should use cache
        intensity2 = await client.get_current_intensity(region="us-west-2")

        # Both should return same timestamp (from cache)
        assert intensity1.timestamp == intensity2.timestamp


@pytest.mark.asyncio
@pytest.mark.integration
async def test_multiple_regions() -> None:
    """Test checking intensity for multiple regions."""
    regions = ["us-west-2", "eu-west-1", "ap-southeast-1"]

    async with CarbonClient() as client:
        for region in regions:
            intensity = await client.get_current_intensity(region=region)
            assert intensity.region == region
            assert intensity.carbon_intensity > 0
