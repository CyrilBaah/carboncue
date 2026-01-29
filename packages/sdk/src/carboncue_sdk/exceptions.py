"""Custom exceptions for CarbonCue SDK."""


class CarbonCueError(Exception):
    """Base exception for all CarbonCue errors."""

    pass


class APIError(CarbonCueError):
    """Error communicating with external API."""

    pass


class InvalidRegionError(CarbonCueError):
    """Invalid cloud region specified."""

    pass


class InvalidProviderError(CarbonCueError):
    """Invalid cloud provider specified."""

    pass


class RateLimitError(APIError):
    """API rate limit exceeded."""

    pass


class AuthenticationError(APIError):
    """API authentication failed."""

    pass


class DataNotAvailableError(APIError):
    """Carbon intensity data not available for requested region."""

    pass
