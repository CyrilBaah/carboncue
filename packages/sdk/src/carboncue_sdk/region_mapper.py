"""Region mapping utilities for cloud providers to Electricity Maps zones."""

from typing import Dict

# Mapping of cloud provider regions to Electricity Maps zone IDs
# Reference: https://static.electricitymap.org/api/docs/index.html#zones
REGION_TO_ZONE_MAP: Dict[str, Dict[str, str]] = {
    "aws": {
        # US Regions
        "us-east-1": "US-VA",  # Virginia
        "us-east-2": "US-MIDA-PJM",  # Ohio
        "us-west-1": "US-CAL-CISO",  # California
        "us-west-2": "US-NW-PACW",  # Oregon
        # EU Regions
        "eu-west-1": "IE",  # Ireland
        "eu-west-2": "GB",  # London
        "eu-west-3": "FR",  # Paris
        "eu-central-1": "DE",  # Frankfurt
        "eu-north-1": "SE",  # Stockholm
        "eu-south-1": "IT-NO",  # Milan
        # Asia Pacific
        "ap-southeast-1": "SG",  # Singapore
        "ap-southeast-2": "AU-NSW",  # Sydney
        "ap-northeast-1": "JP-TK",  # Tokyo
        "ap-northeast-2": "KR",  # Seoul
        "ap-south-1": "IN-WE",  # Mumbai
        # Canada
        "ca-central-1": "CA-ON",  # Montreal
        # South America
        "sa-east-1": "BR-CS",  # São Paulo
    },
    "azure": {
        # US Regions
        "eastus": "US-VA",  # Virginia
        "eastus2": "US-VA",  # Virginia
        "westus": "US-CAL-CISO",  # California
        "westus2": "US-NW-PACW",  # Washington
        "centralus": "US-MIDW-MISO",  # Iowa
        # EU Regions
        "northeurope": "IE",  # Ireland
        "westeurope": "NL",  # Netherlands
        "uksouth": "GB",  # London
        "ukwest": "GB",  # Cardiff
        "francecentral": "FR",  # Paris
        "germanywestcentral": "DE",  # Frankfurt
        "norwayeast": "NO-NO2",  # Norway
        "swedencentral": "SE",  # Sweden
        # Asia Pacific
        "southeastasia": "SG",  # Singapore
        "australiaeast": "AU-NSW",  # Sydney
        "japaneast": "JP-TK",  # Tokyo
        "koreacentral": "KR",  # Seoul
        "centralindia": "IN-WE",  # India
        # Canada
        "canadacentral": "CA-ON",  # Toronto
        # South America
        "brazilsouth": "BR-CS",  # São Paulo
    },
    "gcp": {
        # US Regions
        "us-east1": "US-CAR-SCEG",  # South Carolina
        "us-east4": "US-VA",  # Virginia
        "us-west1": "US-NW-PACW",  # Oregon
        "us-west2": "US-CAL-CISO",  # California
        "us-central1": "US-MIDW-MISO",  # Iowa
        # EU Regions
        "europe-west1": "BE",  # Belgium
        "europe-west2": "GB",  # London
        "europe-west3": "DE",  # Frankfurt
        "europe-west4": "NL",  # Netherlands
        "europe-north1": "FI",  # Finland
        # Asia Pacific
        "asia-southeast1": "SG",  # Singapore
        "asia-northeast1": "JP-TK",  # Tokyo
        "australia-southeast1": "AU-NSW",  # Sydney
        # Canada
        "northamerica-northeast1": "CA-QC",  # Montreal
        # South America
        "southamerica-east1": "BR-CS",  # São Paulo
    },
    "digitalocean": {
        "nyc1": "US-NY-NYIS",  # New York
        "nyc3": "US-NY-NYIS",  # New York
        "sfo2": "US-CAL-CISO",  # San Francisco
        "sfo3": "US-CAL-CISO",  # San Francisco
        "lon1": "GB",  # London
        "ams2": "NL",  # Amsterdam
        "ams3": "NL",  # Amsterdam
        "sgp1": "SG",  # Singapore
        "fra1": "DE",  # Frankfurt
        "tor1": "CA-ON",  # Toronto
        "blr1": "IN-WE",  # Bangalore
        "syd1": "AU-NSW",  # Sydney
    },
}


class RegionMapper:
    """Maps cloud provider regions to Electricity Maps zone identifiers."""

    @staticmethod
    def get_zone_id(region: str, provider: str = "aws") -> str:
        """Get Electricity Maps zone ID for a cloud region.

        Args:
            region: Cloud provider region code (e.g., us-west-2, eastus)
            provider: Cloud provider name (aws, azure, gcp, digitalocean)

        Returns:
            Electricity Maps zone ID (e.g., US-CAL-CISO)

        Raises:
            ValueError: If region or provider is not supported
        """
        provider_lower = provider.lower()

        if provider_lower not in REGION_TO_ZONE_MAP:
            raise ValueError(
                f"Unsupported cloud provider: {provider}. "
                f"Supported: {', '.join(REGION_TO_ZONE_MAP.keys())}"
            )

        region_map = REGION_TO_ZONE_MAP[provider_lower]

        if region not in region_map:
            raise ValueError(
                f"Unsupported region '{region}' for provider '{provider}'. "
                f"Supported regions: {', '.join(region_map.keys())}"
            )

        return region_map[region]

    @staticmethod
    def get_supported_regions(provider: str = "aws") -> list[str]:
        """Get list of supported regions for a cloud provider.

        Args:
            provider: Cloud provider name

        Returns:
            List of supported region codes

        Raises:
            ValueError: If provider is not supported
        """
        provider_lower = provider.lower()

        if provider_lower not in REGION_TO_ZONE_MAP:
            raise ValueError(f"Unsupported cloud provider: {provider}")

        return list(REGION_TO_ZONE_MAP[provider_lower].keys())

    @staticmethod
    def get_supported_providers() -> list[str]:
        """Get list of all supported cloud providers.

        Returns:
            List of supported provider names
        """
        return list(REGION_TO_ZONE_MAP.keys())
