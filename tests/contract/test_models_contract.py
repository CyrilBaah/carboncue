"""Contract tests for CarbonCue SDK API contracts."""

import pytest
from carboncue_sdk.models import CarbonIntensity, Region, SCIScore


class TestCarbonIntensityContract:
    """Contract tests for CarbonIntensity model."""

    def test_carbon_intensity_required_fields(self) -> None:
        """Test that required fields are enforced."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            CarbonIntensity()  # type: ignore

    def test_carbon_intensity_positive_value(self) -> None:
        """Test that carbon intensity must be positive."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            CarbonIntensity(
                region="us-west-2",
                carbon_intensity=-100.0,  # Invalid: must be > 0
                source="test",
            )

    def test_carbon_intensity_percentage_bounds(self) -> None:
        """Test that percentages must be between 0 and 100."""
        # Valid: exactly 0%
        intensity = CarbonIntensity(
            region="us-west-2",
            carbon_intensity=250.0,
            fossil_fuel_percentage=0.0,
            renewable_percentage=100.0,
            source="test",
        )
        assert intensity.renewable_percentage == 100.0

        # Invalid: > 100%
        with pytest.raises(Exception):
            CarbonIntensity(
                region="us-west-2",
                carbon_intensity=250.0,
                fossil_fuel_percentage=150.0,  # Invalid: must be <= 100
                source="test",
            )


class TestSCIScoreContract:
    """Contract tests for SCIScore model."""

    def test_sci_score_required_fields(self) -> None:
        """Test that all required fields are enforced."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            SCIScore()  # type: ignore

    def test_sci_score_positive_values(self) -> None:
        """Test that score and functional unit must be positive."""
        # Valid: positive values
        score = SCIScore(
            score=0.15,
            operational_emissions=100.0,
            embodied_emissions=50.0,
            functional_unit=1000,
            functional_unit_type="requests",
            region="us-west-2",
        )
        assert score.score > 0

        # Invalid: zero functional unit
        with pytest.raises(Exception):
            SCIScore(
                score=0.15,
                operational_emissions=100.0,
                embodied_emissions=50.0,
                functional_unit=0,  # Invalid: must be > 0
                functional_unit_type="requests",
                region="us-west-2",
            )

    def test_sci_score_non_negative_emissions(self) -> None:
        """Test that emissions cannot be negative."""
        # Valid: zero emissions
        score = SCIScore(
            score=0.0,
            operational_emissions=0.0,
            embodied_emissions=0.0,
            functional_unit=1000,
            functional_unit_type="requests",
            region="us-west-2",
        )
        assert score.operational_emissions == 0.0

        # Invalid: negative emissions
        with pytest.raises(Exception):
            SCIScore(
                score=0.15,
                operational_emissions=-100.0,  # Invalid: must be >= 0
                embodied_emissions=50.0,
                functional_unit=1000,
                functional_unit_type="requests",
                region="us-west-2",
            )


class TestRegionContract:
    """Contract tests for Region model."""

    def test_region_required_fields(self) -> None:
        """Test that code and provider are required."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            Region()  # type: ignore

    def test_region_valid_providers(self) -> None:
        """Test that only valid cloud providers are accepted."""
        # Valid providers
        for provider in ["aws", "azure", "gcp", "digitalocean", "other"]:
            region = Region(code="us-west-2", provider=provider)  # type: ignore
            assert region.provider == provider

        # Invalid provider
        with pytest.raises(Exception):
            Region(code="us-west-2", provider="invalid-provider")  # type: ignore

    def test_region_immutable(self) -> None:
        """Test that Region is immutable."""
        region = Region(code="us-west-2", provider="aws")

        with pytest.raises(Exception):
            region.code = "eu-west-1"  # type: ignore
