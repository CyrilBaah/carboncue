"""Unit tests for region mapper."""

import pytest
from carboncue_sdk.region_mapper import RegionMapper


class TestRegionMapper:
    """Test suite for RegionMapper."""

    def test_get_zone_id_aws(self) -> None:
        """Test mapping AWS regions to zones."""
        assert RegionMapper.get_zone_id("us-west-2", "aws") == "US-NW-PACW"
        assert RegionMapper.get_zone_id("us-east-1", "aws") == "US-VA"
        assert RegionMapper.get_zone_id("eu-west-1", "aws") == "IE"

    def test_get_zone_id_azure(self) -> None:
        """Test mapping Azure regions to zones."""
        assert RegionMapper.get_zone_id("eastus", "azure") == "US-VA"
        assert RegionMapper.get_zone_id("westeurope", "azure") == "NL"
        assert RegionMapper.get_zone_id("uksouth", "azure") == "GB"

    def test_get_zone_id_gcp(self) -> None:
        """Test mapping GCP regions to zones."""
        assert RegionMapper.get_zone_id("us-west1", "gcp") == "US-NW-PACW"
        assert RegionMapper.get_zone_id("europe-west1", "gcp") == "BE"
        assert RegionMapper.get_zone_id("asia-southeast1", "gcp") == "SG"

    def test_get_zone_id_case_insensitive(self) -> None:
        """Test that provider matching is case-insensitive."""
        assert RegionMapper.get_zone_id("us-west-2", "AWS") == "US-NW-PACW"
        assert RegionMapper.get_zone_id("us-west-2", "Aws") == "US-NW-PACW"

    def test_get_zone_id_invalid_provider(self) -> None:
        """Test that invalid provider raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported cloud provider"):
            RegionMapper.get_zone_id("us-west-2", "invalid")

    def test_get_zone_id_invalid_region(self) -> None:
        """Test that invalid region raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported region"):
            RegionMapper.get_zone_id("invalid-region", "aws")

    def test_get_supported_regions_aws(self) -> None:
        """Test getting supported AWS regions."""
        regions = RegionMapper.get_supported_regions("aws")
        assert isinstance(regions, list)
        assert "us-west-2" in regions
        assert "us-east-1" in regions
        assert "eu-west-1" in regions

    def test_get_supported_regions_azure(self) -> None:
        """Test getting supported Azure regions."""
        regions = RegionMapper.get_supported_regions("azure")
        assert isinstance(regions, list)
        assert "eastus" in regions
        assert "westeurope" in regions

    def test_get_supported_regions_invalid_provider(self) -> None:
        """Test that invalid provider raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported cloud provider"):
            RegionMapper.get_supported_regions("invalid")

    def test_get_supported_providers(self) -> None:
        """Test getting all supported providers."""
        providers = RegionMapper.get_supported_providers()
        assert isinstance(providers, list)
        assert "aws" in providers
        assert "azure" in providers
        assert "gcp" in providers
        assert "digitalocean" in providers
