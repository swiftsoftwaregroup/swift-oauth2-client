class OAuth2ClientError(Exception):
    """Base exception for OAuth2Client."""

class TokenRefreshError(OAuth2ClientError):
    """Raised when token refresh fails."""

class APIError(OAuth2ClientError):
    """Raised when an API call fails."""