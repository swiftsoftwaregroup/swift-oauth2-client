"""
This module provides a class for managing OAuth2 tokens.
"""
import base64
import time
import asyncio
import httpx
from .config import OAuth2Config
from .exceptions import TokenRefreshError

class TokenManagerAsync:
    """
    Manages OAuth2 token acquisition and renewal.

    This class is responsible for obtaining and refreshing OAuth2 tokens
    as needed for API authentication.

    Attributes:
        config (OAuth2Config): The OAuth2 configuration.
        access_token (str): The current access token.
        expires_at (float): The expiration time of the current token.
        lock (asyncio.Lock): A lock for thread-safe token refresh operations.

    Example:
        ```python
        config = OAuth2Config(...)
        token_manager = TokenManagerAsync(config)
        token = await token_manager.get_valid_token()
        ```
    """

    def __init__(self, config: OAuth2Config):
        """
        Initialize the TokenManagerAsync.

        Args:
            config (OAuth2Config): The OAuth2 configuration.
        """
        self.config = config
        self.access_token = None
        self.expires_at = 0
        self.lock = asyncio.Lock()

    async def get_valid_token(self) -> str:
        """
        Get a valid OAuth2 token, refreshing if necessary.

        Returns:
            str: A valid OAuth2 access token.

        Raises:
            TokenRefreshError: If token refresh fails.
        """
        async with self.lock:
            if time.time() >= self.expires_at:
                await self.refresh_token()
            return self.access_token

    async def refresh_token(self):
        """
        Refresh the OAuth2 token.

        This method obtains a new access token from the OAuth2 server.

        Raises:
            TokenRefreshError: If token refresh fails.
        """
        auth = base64.b64encode(f"{self.config.client_id}:{self.config.client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "scope": " ".join(self.config.scopes)
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.config.token_url, headers=headers, data=data)
                response.raise_for_status()
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.expires_at = time.time() + token_data["expires_in"] - 60  # Refresh 1 minute before expiration
            except httpx.HTTPStatusError as e:
                raise TokenRefreshError(f"Failed to refresh token: {e}") from e
