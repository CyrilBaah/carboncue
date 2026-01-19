"""Configuration management for CarbonCue SDK."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class CarbonConfig(BaseSettings):
    """Configuration for CarbonCue SDK.

    All settings can be provided via environment variables with CARBONCUE_ prefix.
    Example: CARBONCUE_ELECTRICITY_MAPS_API_KEY=your_key
    """

    model_config = SettingsConfigDict(
        env_prefix="CARBONCUE_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API Configuration
    electricity_maps_api_key: str | None = None
    electricity_maps_base_url: str = "https://api.electricitymap.org/v3"

    # GSF Carbon-Aware SDK Configuration
    carbon_aware_sdk_url: str | None = None
    use_carbon_aware_sdk: bool = False

    # Default Settings
    default_region: str = "us-west-2"
    default_cloud_provider: str = "aws"

    # Request Configuration
    request_timeout: int = 30
    max_retries: int = 3

    # Cache Configuration
    cache_ttl_seconds: int = 300  # 5 minutes
    enable_caching: bool = True
