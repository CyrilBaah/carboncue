"""Unit tests for CarbonCue SDK client."""

from datetime import datetime

import pytest
from carboncue_sdk import CarbonClient, CarbonConfig
from carboncue_sdk.models import CarbonIntensity, SCIScore


@pytest.fixture
def client() -> CarbonClient:
    """Create a test client with mock configuration."""
    config = CarbonConfig(
        electricity_maps_api_key="test-key",
        enable_caching=False,  # Disable caching for tests
    )
    return CarbonClient(config=config)


class TestCarbonClient:
    """Test suite for CarbonClient."""

    def test_calculate_sci_basic(self, client: CarbonClient) -> None:
        """Test basic SCI calculation."""
        score = client.calculate_sci(
            operational_emissions=100.0,
            embodied_emissions=50.0,
            functional_unit=1000,
            functional_unit_type="requests",
            region="us-west-2",
        )

        assert isinstance(score, SCIScore)
        assert score.score == 0.15  # (100 + 50) / 1000
        assert score.operational_emissions == 100.0
        assert score.embodied_emissions == 50.0
        assert score.functional_unit == 1000
        assert score.functional_unit_type == "requests"
        assert score.region == "us-west-2"

    def test_calculate_sci_zero_functional_unit(self, client: CarbonClient) -> None:
        """Test SCI calculation with zero functional unit raises error."""
        with pytest.raises(ValueError, match="Functional unit must be greater than 0"):
            client.calculate_sci(
                operational_emissions=100.0,
                embodied_emissions=50.0,
                functional_unit=0,
                functional_unit_type="requests",
            )

    def test_calculate_sci_negative_functional_unit(self, client: CarbonClient) -> None:
        """Test SCI calculation with negative functional unit raises error."""
        with pytest.raises(ValueError, match="Functional unit must be greater than 0"):
            client.calculate_sci(
                operational_emissions=100.0,
                embodied_emissions=50.0,
                functional_unit=-10,
                functional_unit_type="requests",
            )

    def test_calculate_sci_zero_emissions(self, client: CarbonClient) -> None:
        """Test SCI calculation with zero emissions."""
        score = client.calculate_sci(
            operational_emissions=0.0,
            embodied_emissions=0.0,
            functional_unit=1000,
            functional_unit_type="requests",
        )

        assert score.score == 0.0
        assert score.operational_emissions == 0.0
        assert score.embodied_emissions == 0.0

    @pytest.mark.asyncio
    async def test_get_current_intensity(self, client: CarbonClient) -> None:
        """Test getting current carbon intensity."""
        async with client:
            intensity = await client.get_current_intensity(region="us-west-2", provider="aws")

        assert isinstance(intensity, CarbonIntensity)
        assert intensity.region == "us-west-2"
        assert intensity.carbon_intensity > 0
        assert isinstance(intensity.timestamp, datetime)
        assert intensity.source == "mock"  # Currently using mock data

    @pytest.mark.asyncio
    async def test_context_manager(self) -> None:
        """Test async context manager."""
        config = CarbonConfig(electricity_maps_api_key="test")
        async with CarbonClient(config=config) as client:
            assert client._http_client is not None

        # Client should be closed after context
        assert client._http_client is None


class TestCarbonIntensity:
    """Test suite for CarbonIntensity model."""

    def test_carbon_intensity_creation(self) -> None:
        """Test creating a CarbonIntensity instance."""
        intensity = CarbonIntensity(
            region="us-west-2",
            carbon_intensity=250.5,
            fossil_fuel_percentage=60.0,
            renewable_percentage=40.0,
            source="ElectricityMaps",
        )

        assert intensity.region == "us-west-2"
        assert intensity.carbon_intensity == 250.5
        assert intensity.fossil_fuel_percentage == 60.0
        assert intensity.renewable_percentage == 40.0
        assert intensity.source == "ElectricityMaps"

    def test_carbon_intensity_immutable(self) -> None:
        """Test that CarbonIntensity is immutable (frozen)."""
        intensity = CarbonIntensity(
            region="us-west-2",
            carbon_intensity=250.0,
            source="test",
        )

        with pytest.raises(Exception):  # Pydantic ValidationError
            intensity.carbon_intensity = 300.0  # type: ignore


class TestSCIScore:
    """Test suite for SCIScore model."""

    def test_sci_score_creation(self) -> None:
        """Test creating an SCIScore instance."""
        score = SCIScore(
            score=0.15,
            operational_emissions=100.0,
            embodied_emissions=50.0,
            functional_unit=1000,
            functional_unit_type="requests",
            region="us-west-2",
        )

        assert score.score == 0.15
        assert score.operational_emissions == 100.0
        assert score.embodied_emissions == 50.0
        assert score.functional_unit == 1000
        assert score.functional_unit_type == "requests"
        assert score.region == "us-west-2"

    def test_sci_score_immutable(self) -> None:
        """Test that SCIScore is immutable (frozen)."""
        score = SCIScore(
            score=0.15,
            operational_emissions=100.0,
            embodied_emissions=50.0,
            functional_unit=1000,
            functional_unit_type="requests",
            region="us-west-2",
        )

        with pytest.raises(Exception):  # Pydantic ValidationError
            score.score = 0.20  # type: ignore
